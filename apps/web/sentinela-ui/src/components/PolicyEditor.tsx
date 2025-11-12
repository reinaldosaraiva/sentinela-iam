'use client';

import { useState, useEffect } from 'react';
import { Save, Play, Eye, Copy, Download, Upload, CheckCircle, AlertCircle } from 'lucide-react';

interface Policy {
  id: string;
  name: string;
  description: string;
  content: string;
  status: 'active' | 'inactive' | 'draft';
  created_at: string;
  updated_at: string;
}

interface PolicyEditorProps {
  policy?: Policy;
  onSave?: (policy: Partial<Policy>) => void;
  onTest?: (policy: string) => void;
}

export default function PolicyEditor({ policy, onSave, onTest }: PolicyEditorProps) {
  const [content, setContent] = useState(policy?.content || '');
  const [name, setName] = useState(policy?.name || '');
  const [description, setDescription] = useState(policy?.description || '');
  const [status, setStatus] = useState<'active' | 'inactive' | 'draft'>(policy?.status || 'draft');
  const [isValid, setIsValid] = useState(true);
  const [testResult, setTestResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Sample Cedar policy template
  const samplePolicy = `# Cedar Policy for Document Access
# Define entities and their attributes

entity User {
  role: String,
  department: String,
  clearance_level: Integer
}

entity Document {
  classification: String,
  department: String,
  owner: String
}

entity Action {}

# Define permissions
rule "allow_read_document" {
  permit when {
    # Users can read documents from their department
    action.name == "read" &&
    resource.department == principal.department &&
    principal.clearance_level >= 1
  }
}

rule "allow_write_document" {
  permit when {
    # Users can write documents they own
    action.name == "write" &&
    resource.owner == principal.id
  } or {
    # Managers can write any document in their department
    action.name == "write" &&
    principal.role == "manager" &&
    resource.department == principal.department
  }
}

rule "allow_admin_access" {
  permit when {
    # Admins can access any document
    principal.role == "admin"
  }
}`;

  useEffect(() => {
    // Basic validation for Cedar syntax
    const validatePolicy = () => {
      try {
        // Simple validation - check for basic Cedar structure
        const hasEntity = content.includes('entity ');
        const hasRule = content.includes('rule ');
        setIsValid(hasEntity && hasRule);
      } catch (error) {
        setIsValid(false);
      }
    };

    const timer = setTimeout(validatePolicy, 500);
    return () => clearTimeout(timer);
  }, [content]);

  const handleSave = () => {
    const policyData = {
      name,
      description,
      content,
      status
    };
    onSave?.(policyData);
  };

  const handleTest = async () => {
    setIsLoading(true);
    try {
      const result = await onTest?.(content);
      setTestResult(result);
    } catch (error) {
      setTestResult({ error: error.message });
    } finally {
      setIsLoading(false);
    }
  };

  const loadSample = () => {
    setContent(samplePolicy);
    setName('Sample Document Access Policy');
    setDescription('Sample policy demonstrating document access controls');
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="border-b border-gray-200 p-4">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${isValid ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-sm text-gray-600">
              {isValid ? 'Valid Cedar syntax' : 'Invalid Cedar syntax'}
            </span>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={loadSample}
              className="px-3 py-1 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
            >
              Load Sample
            </button>
            <button
              onClick={() => navigator.clipboard.writeText(content)}
              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
              title="Copy to clipboard"
            >
              <Copy className="w-4 h-4" />
            </button>
            <button
              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
              title="Download policy"
            >
              <Download className="w-4 h-4" />
            </button>
            <button
              className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
              title="Upload policy"
            >
              <Upload className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Policy Metadata */}
        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Policy Name
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter policy name"
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
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter policy description"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value as any)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="draft">Draft</option>
              <option value="inactive">Inactive</option>
              <option value="active">Active</option>
            </select>
          </div>
        </div>
      </div>

      {/* Editor */}
      <div className="flex-1 flex">
        <div className="flex-1 relative">
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="w-full h-full p-4 font-mono text-sm bg-gray-50 border-0 resize-none focus:outline-none"
            placeholder="Enter your Cedar policy here..."
            spellCheck={false}
          />
        </div>

        {/* Test Results Panel */}
        {testResult && (
          <div className="w-80 border-l border-gray-200 bg-gray-50 p-4 overflow-y-auto">
            <h3 className="font-medium text-gray-900 mb-3">Test Results</h3>
            
            {testResult.error ? (
              <div className="flex items-start space-x-2 text-red-600">
                <AlertCircle className="w-4 h-4 mt-0.5" />
                <span className="text-sm">{testResult.error}</span>
              </div>
            ) : (
              <div className="space-y-3">
                <div className="flex items-center space-x-2 text-green-600">
                  <CheckCircle className="w-4 h-4" />
                  <span className="text-sm font-medium">Policy test passed</span>
                </div>
                
                {testResult.results && (
                  <div className="space-y-2">
                    {testResult.results.map((result: any, index: number) => (
                      <div key={index} className="p-2 bg-white rounded border border-gray-200">
                        <div className="text-xs font-medium text-gray-700 mb-1">
                          Test Case {index + 1}
                        </div>
                        <div className="text-xs text-gray-600">
                          {result.action} on {result.resource} by {result.principal}
                        </div>
                        <div className={`text-xs font-medium mt-1 ${
                          result.allowed ? 'text-green-600' : 'text-red-600'
                        }`}>
                          {result.allowed ? 'ALLOWED' : 'DENIED'}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Footer Actions */}
      <div className="border-t border-gray-200 p-4 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <button
            onClick={handleTest}
            disabled={isLoading || !isValid}
            className="flex items-center space-x-2 px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Play className="w-4 h-4" />
            <span>{isLoading ? 'Testing...' : 'Test Policy'}</span>
          </button>
          
          <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors">
            <Eye className="w-4 h-4" />
            <span>Preview</span>
          </button>
        </div>

        <div className="flex items-center space-x-2">
          <button className="px-4 py-2 text-gray-600 hover:text-gray-900 transition-colors">
            Cancel
          </button>
          <button
            onClick={handleSave}
            disabled={!isValid}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Save className="w-4 h-4" />
            <span>Save Policy</span>
          </button>
        </div>
      </div>
    </div>
  );
}