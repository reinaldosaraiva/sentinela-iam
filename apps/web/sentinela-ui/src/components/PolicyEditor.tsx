'use client';

import CedarPolicyEditor from './CedarPolicyEditor';

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
  onTest?: (policy: string) => Promise<any>;
}

export default function PolicyEditor({ policy, onSave, onTest }: PolicyEditorProps) {
  return (
    <CedarPolicyEditor
      policy={policy}
      onSave={onSave}
      onTest={onTest}
    />
  );
}