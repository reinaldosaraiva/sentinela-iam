'use client';

import { useState, useEffect, useRef } from 'react';
import { showToast } from '@/lib/toast';
import Editor from '@monaco-editor/react';
import { Save, Play, Eye, Copy, Download, Upload, CheckCircle, AlertCircle, Clock, FileText, Settings } from 'lucide-react';

interface Policy {
  id: string;
  name: string;
  description: string;
  content: string;
  status: 'active' | 'inactive' | 'draft';
  created_at: string;
  updated_at: string;
  version?: string;
}

interface CedarPolicyEditorProps {
  policy?: Policy;
  onSave?: (policy: Partial<Policy>) => void;
  onTest?: (policy: string) => Promise<any>;
}

// Cedar language definition for Monaco
const cedarLanguageDefinition = {
  // Basic keywords
  keywords: [
    'policy', 'permit', 'forbid', 'when', 'has', 'in', 'if', 'else', 'unless',
    'rule', 'entity', 'type', 'namespace', 'use', 'as', 'principal', 'action', 'resource'
  ],
  
  // Types
  types: [
    'String', 'Boolean', 'Integer', 'Long', 'Double', 'Set', 'Entity', 'Record',
    'Extension', 'Decimal'
  ],
  
  // Built-in functions
  functions: [
    'size', 'contains', 'startsWith', 'endsWith', 'substring', 'split', 'join',
    'toLowerCase', 'toUpperCase', 'trim', 'matches', 'abs', 'ceil', 'floor',
    'round', 'min', 'max', 'sum', 'average', 'now', 'duration', 'parseDuration',
    'formatDuration', 'parseIPAddress', 'isIPAddress', 'parseCIDR', 'isCIDR',
    'isIpv4', 'isIpv6', 'lessThan', 'lessThanOrEqual', 'greaterThan',
    'greaterThanOrEqual', 'plus', 'minus', 'times', 'dividedBy', 'mod'
  ],
  
  // Operators
  operators: [
    '==', '!=', '<', '<=', '>', '>=', '&&', '||', '!', '&&', '||',
    '+', '-', '*', '/', '%', 'in', 'has', 'like', 'contains'
  ]
};

export default function CedarPolicyEditor({ policy, onSave, onTest }: CedarPolicyEditorProps) {
  const [content, setContent] = useState(policy?.content || getDefaultPolicyTemplate());
  const [name, setName] = useState(policy?.name || '');
  const [description, setDescription] = useState(policy?.description || '');
  const [status, setStatus] = useState<'active' | 'inactive' | 'draft'>(policy?.status || 'draft');
  const [isValid, setIsValid] = useState(true);
  const [testResult, setTestResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [wordWrap, setWordWrap] = useState(true);
  const [minimap, setMinimap] = useState(true);
  const [fontSize, setFontSize] = useState(14);
  const editorRef = useRef<any>(null);

  function getDefaultPolicyTemplate() {
    return `# Cedar Policy Template
# Define entities and their attributes

entity User {
  role: String,
  department: String,
  clearance_level: Integer,
  is_active: Boolean
}

entity Document {
  classification: String,
  department: String,
  owner: String,
  created_at: Long
}

entity Action {}

# Policy rules
policy "allow_read_document" {
  permit(
    principal in User::"alice",
    action in Action::"read",
    resource in Document::"public"
  );
}

policy "allow_admin_full_access" {
  permit(
    principal,
    action,
    resource
  ) when {
    principal.role == "admin" && 
    principal.is_active == true
  };
}

policy "allow_department_access" {
  permit(
    principal: User,
    action: Action,
    resource: Document
  ) when {
    principal.department == resource.department &&
    principal.clearance_level >= 3
  };
}`;
  }

  useEffect(() => {
    // Configure Monaco for Cedar language
    const configureMonaco = (monaco: any) => {
      // Register Cedar language
      monaco.languages.register({ id: 'cedar' });

      // Define language tokens
      monaco.languages.setMonarchTokensProvider('cedar', {
        tokenizer: {
          root: [
            // Comments
            [/#.*$/, 'comment'],
            
            // Strings
            [/"([^"\\]|\\.)*$/, 'string.invalid'],
            [/"/, 'string', '@string_double'],
            
            // Keywords
            [/[a-zA-Z_]\w*/, {
              cases: {
                '@keywords': 'keyword',
                '@types': 'type',
                '@functions': 'function.identifier',
                '@default': 'identifier'
              }
            }],
            
            // Numbers
            [/\d*\.\d+([eE][\-+]?\d+)?/, 'number.float'],
            [/0[xX][0-9a-fA-F]+/, 'number.hex'],
            [/\d+/, 'number'],
            
            // Operators
            [/[+\-*\/%=<>!&|^~?:]/, 'operators'],
            
            // Brackets
            [/[{}()\[\]]/, '@brackets'],
            
            // Punctuation
            [/[;,.]/, 'delimiter'],
            
            // Whitespace
            [/\s+/, 'white']
          ],
          
          string_double: [
            [/[^\\"]+/, 'string'],
            [/\\./, 'string.escape'],
            [/"/, 'string', '@pop']
          ]
        },
        
        keywords: cedarLanguageDefinition.keywords,
        types: cedarLanguageDefinition.types,
        functions: cedarLanguageDefinition.functions,
        operators: cedarLanguageDefinition.operators
      });

      // Set theme for Cedar
      monaco.editor.defineTheme('cedar-dark', {
        base: 'vs-dark',
        inherit: true,
        rules: [
          { token: 'comment', foreground: '6A9955', fontStyle: 'italic' },
          { token: 'keyword', foreground: '569CD6' },
          { token: 'type', foreground: '4EC9B0' },
          { token: 'function.identifier', foreground: 'DCDCAA' },
          { token: 'string', foreground: 'CE9178' },
          { token: 'number', foreground: 'B5CEA8' },
          { token: 'operators', foreground: 'D4D4D4' },
          { token: 'identifier', foreground: '9CDCFE' },
          { token: 'delimiter', foreground: 'D4D4D4' }
        ],
        colors: {
          'editor.background': '#1E1E1E',
          'editor.foreground': '#D4D4D4',
          'editorCursor.foreground': '#AEAFAD',
          'editor.lineHighlightBackground': '#2D2D30',
          'editorLineNumber.foreground': '#858585',
          'editor.selectionBackground': '#264F78',
          'editor.inactiveSelectionBackground': '#3A3D41'
        }
      });

      // Set language configuration
      monaco.languages.setLanguageConfiguration('cedar', {
        comments: {
          lineComment: '#',
        },
        brackets: [
          ['{', '}'],
          ['[', ']'],
          ['(', ')']
        ],
        autoClosingPairs: [
          { open: '{', close: '}' },
          { open: '[', close: ']' },
          { open: '(', close: ')' },
          { open: '"', close: '"' }
        ],
        surroundingPairs: [
          { open: '{', close: '}' },
          { open: '[', close: ']' },
          { open: '(', close: ')' },
          { open: '"', close: '"' }
        ]
      });
    };

    // Load Monaco and configure
    import('monaco-editor').then((monaco) => {
      configureMonaco(monaco);
    });
  }, []);

  const handleSave = async () => {
    if (!name.trim()) {
      showToast.error('Please enter a policy name');
      return;
    }

    setIsLoading(true);
    try {
      await onSave?.({
        name: name.trim(),
        description: description.trim(),
        content: content.trim(),
        status
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleTest = async () => {
    setIsLoading(true);
    try {
      const result = await onTest?.(content);
      setTestResult(result);
      setShowPreview(true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopyTemplate = () => {
    navigator.clipboard.writeText(getDefaultPolicyTemplate());
    showToast.success('Template copied to clipboard!');
  };

  const handleDownload = () => {
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${name || 'policy'}.cedar`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target?.result as string;
        setContent(content);
      };
      reader.readAsText(file);
    }
  };

  const validateSyntax = () => {
    // Basic syntax validation
    const lines = content.split('\n');
    let hasError = false;
    
    lines.forEach((line, index) => {
      const trimmed = line.trim();
      if (trimmed && !trimmed.startsWith('#')) {
        // Check for basic policy structure
        if (trimmed.includes('policy') && !trimmed.includes('{')) {
          hasError = true;
        }
      }
    });
    
    setIsValid(!hasError);
  };

  useEffect(() => {
    validateSyntax();
  }, [content]);

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Header */}
      <div className="border-b border-gray-200 p-4">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <FileText className="w-5 h-5 text-blue-600" />
            <h2 className="text-lg font-semibold text-gray-900">
              {policy ? 'Edit Policy' : 'Create Policy'}
            </h2>
            {isValid ? (
              <CheckCircle className="w-4 h-4 text-green-500" />
            ) : (
              <AlertCircle className="w-4 h-4 text-red-500" />
            )}
          </div>
          
          <div className="flex items-center gap-2">
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
              title="Settings"
            >
              <Settings className="w-4 h-4" />
            </button>
            <button
              onClick={handleCopyTemplate}
              className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
              title="Copy Template"
            >
              <Copy className="w-4 h-4" />
            </button>
            <label className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors cursor-pointer" title="Upload File">
              <Upload className="w-4 h-4" />
              <input type="file" accept=".cedar,.txt" onChange={handleUpload} className="hidden" />
            </label>
            <button
              onClick={handleDownload}
              className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
              title="Download"
            >
              <Download className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Settings Panel */}
        {showSettings && (
          <div className="mb-4 p-3 bg-gray-50 rounded-lg">
            <div className="grid grid-cols-3 gap-4">
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={wordWrap}
                  onChange={(e) => setWordWrap(e.target.checked)}
                  className="rounded"
                />
                <span className="text-sm">Word Wrap</span>
              </label>
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={minimap}
                  onChange={(e) => setMinimap(e.target.checked)}
                  className="rounded"
                />
                <span className="text-sm">Minimap</span>
              </label>
              <div className="flex items-center gap-2">
                <label className="text-sm">Font Size:</label>
                <input
                  type="number"
                  min="10"
                  max="20"
                  value={fontSize}
                  onChange={(e) => setFontSize(Number(e.target.value))}
                  className="w-16 px-2 py-1 border rounded"
                />
              </div>
            </div>
          </div>
        )}

        {/* Policy Metadata */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Policy Name *
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="e.g., Document Access Policy"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <input
              type="text"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Brief description of the policy"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value as any)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="draft">Draft</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>
        </div>
      </div>

      {/* Editor */}
      <div className="flex-1 flex">
        <div className="flex-1">
          <Editor
            height="100%"
            language="cedar"
            theme="cedar-dark"
            value={content}
            onChange={(value) => setContent(value || '')}
            onMount={(editor) => {
              editorRef.current = editor;
              editor.focus();
            }}
              options={{
                minimap: { enabled: minimap },
                wordWrap: wordWrap ? 'on' : 'off',
                fontSize: fontSize,
                lineNumbers: 'on',
                scrollBeyondLastLine: false,
                automaticLayout: true,
                tabSize: 2,
                insertSpaces: true,
                folding: true,
                foldingStrategy: 'indentation',
                showFoldingControls: 'always',
                padding: { top: 16, bottom: 16 },
                suggestOnTriggerCharacters: true,
                quickSuggestions: true,
                parameterHints: { enabled: true },
                acceptSuggestionOnEnter: 'on',
                tabCompletion: 'on',
                wordBasedSuggestions: true
              }}
          />
        </div>

        {/* Test Results Panel */}
        {showPreview && testResult && (
          <div className="w-96 border-l border-gray-200 bg-gray-50">
            <div className="p-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <h3 className="font-medium text-gray-900">Test Results</h3>
                <button
                  onClick={() => setShowPreview(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ×
                </button>
              </div>
            </div>
            
            <div className="p-4">
              {testResult.summary && (
                <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                  <div className="text-sm font-medium text-blue-900">Summary</div>
                  <div className="text-xs text-blue-700 mt-1">
                    Total: {testResult.summary.total} | 
                    Allowed: {testResult.summary.allowed} | 
                    Denied: {testResult.summary.denied}
                  </div>
                </div>
              )}
              
              {testResult.results && (
                <div className="space-y-3">
                  {testResult.results.map((result: any, index: number) => (
                    <div key={index} className="p-3 bg-white rounded-lg border">
                      <div className="flex items-center gap-2 mb-2">
                        {result.allowed ? (
                          <CheckCircle className="w-4 h-4 text-green-500" />
                        ) : (
                          <AlertCircle className="w-4 h-4 text-red-500" />
                        )}
                        <span className="text-sm font-medium">
                          {result.allowed ? 'Allowed' : 'Denied'}
                        </span>
                      </div>
                      <div className="text-xs text-gray-600 space-y-1">
                        <div>Principal: {result.principal}</div>
                        <div>Action: {result.action}</div>
                        <div>Resource: {result.resource}</div>
                        {result.reason && (
                          <div className="text-gray-500">Reason: {result.reason}</div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Footer Actions */}
      <div className="border-t border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-500">
            Cedar Policy Language • {content.split('\n').length} lines
          </div>
          
          <div className="flex items-center gap-3">
            <button
              onClick={handleTest}
              disabled={isLoading || !isValid}
              className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Play className="w-4 h-4" />
              {isLoading ? 'Testing...' : 'Test Policy'}
            </button>
            
            <button
              onClick={handleSave}
              disabled={isLoading || !isValid || !name.trim()}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Save className="w-4 h-4" />
              {isLoading ? 'Saving...' : 'Save Policy'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}