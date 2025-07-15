import React, { useRef, useEffect, useState } from 'react';
import { Editor as MonacoEditorComponent, loader } from '@monaco-editor/react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '@/store';
import { updateFileContent, setCursorPosition } from '@/store/slices/editorSlice';
import { editor } from 'monaco-editor';
import { debounce } from '@/utils';

interface MonacoEditorProps {
  fileId: string;
  content: string;
  language: string;
  readOnly?: boolean;
  onContentChange?: (content: string) => void;
}

const MonacoEditor: React.FC<MonacoEditorProps> = ({
  fileId,
  content,
  language,
  readOnly = false,
  onContentChange,
}) => {
  const dispatch = useDispatch();
  const editorRef = useRef<editor.IStandaloneCodeEditor | null>(null);
  const { settings } = useSelector((state: RootState) => state.editor);
  const [isEditorReady, setIsEditorReady] = useState(false);

  // Configure Monaco Editor
  useEffect(() => {
    loader.config({
      paths: {
        vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.44.0/min/vs',
      },
    });

    loader.init().then((monaco) => {
      // Configure themes
      monaco.editor.defineTheme('omnidev-dark', {
        base: 'vs-dark',
        inherit: true,
        rules: [
          { token: 'comment', foreground: '6A9955' },
          { token: 'keyword', foreground: '569CD6' },
          { token: 'string', foreground: 'CE9178' },
          { token: 'number', foreground: 'B5CEA8' },
          { token: 'type', foreground: '4EC9B0' },
          { token: 'function', foreground: 'DCDCAA' },
          { token: 'variable', foreground: '9CDCFE' },
        ],
        colors: {
          'editor.background': '#0D1117',
          'editor.foreground': '#C9D1D9',
          'editor.lineHighlightBackground': '#161B22',
          'editor.selectionBackground': '#264F78',
          'editor.inactiveSelectionBackground': '#3A3D41',
          'editorCursor.foreground': '#C9D1D9',
          'editorWhitespace.foreground': '#484F58',
          'editorIndentGuide.background': '#21262D',
          'editorIndentGuide.activeBackground': '#30363D',
          'editorLineNumber.foreground': '#6E7681',
          'editorLineNumber.activeForeground': '#C9D1D9',
        },
      });

      // Set default theme
      monaco.editor.setTheme('omnidev-dark');
    });
  }, []);

  // Debounced content change handler
  const debouncedContentChange = debounce((newContent: string) => {
    dispatch(updateFileContent({ fileId, content: newContent }));
    onContentChange?.(newContent);
  }, 300);

  const handleEditorDidMount = (
    editor: editor.IStandaloneCodeEditor,
    monaco: typeof import('monaco-editor')
  ) => {
    editorRef.current = editor;
    setIsEditorReady(true);

    // Configure editor options
    editor.updateOptions({
      fontSize: settings.fontSize,
      tabSize: settings.tabSize,
      wordWrap: settings.wordWrap,
      minimap: { enabled: settings.minimap },
      lineNumbers: settings.lineNumbers,
      automaticLayout: true,
      scrollBeyondLastLine: false,
      readOnly,
    });

    // Handle cursor position changes
    editor.onDidChangeCursorPosition((e) => {
      dispatch(setCursorPosition({
        fileId,
        line: e.position.lineNumber,
        column: e.position.column,
      }));
    });

    // Handle content changes
    editor.onDidChangeModelContent(() => {
      const newContent = editor.getValue();
      debouncedContentChange(newContent);
    });

    // Add keyboard shortcuts
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
      // Save file
      console.log('Save file:', fileId);
    });

    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyD, () => {
      // Duplicate line
      editor.trigger('keyboard', 'editor.action.copyLinesDownAction', {});
    });

    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Slash, () => {
      // Toggle line comment
      editor.trigger('keyboard', 'editor.action.commentLine', {});
    });

    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.KeyK, () => {
      // Delete line
      editor.trigger('keyboard', 'editor.action.deleteLines', {});
    });

    // Focus editor
    editor.focus();
  };

  // Update editor options when settings change
  useEffect(() => {
    if (editorRef.current) {
      editorRef.current.updateOptions({
        fontSize: settings.fontSize,
        tabSize: settings.tabSize,
        wordWrap: settings.wordWrap,
        minimap: { enabled: settings.minimap },
        lineNumbers: settings.lineNumbers,
      });
    }
  }, [settings]);

  // Update theme when settings change
  useEffect(() => {
    if (isEditorReady) {
      loader.init().then((monaco) => {
        monaco.editor.setTheme(settings.theme === 'vs-dark' ? 'omnidev-dark' : settings.theme);
      });
    }
  }, [settings.theme, isEditorReady]);

  return (
    <div className="h-full w-full bg-gray-900">
      <MonacoEditorComponent
        height="100%"
        language={language}
        value={content}
        theme="omnidev-dark"
        onMount={handleEditorDidMount}
        options={{
          selectOnLineNumbers: true,
          automaticLayout: true,
          scrollBeyondLastLine: false,
          readOnly,
          fontSize: settings.fontSize,
          tabSize: settings.tabSize,
          wordWrap: settings.wordWrap,
          minimap: { enabled: settings.minimap },
          lineNumbers: settings.lineNumbers,
          bracketPairColorization: { enabled: true } as any,
          guides: {
            bracketPairs: true,
            indentation: true,
          },
          suggest: {
            showKeywords: true,
            showSnippets: true,
          },
          quickSuggestions: {
            other: "on" as const,
            comments: "on" as const,
            strings: "on" as const,
          },
          folding: true,
          foldingStrategy: 'indentation',
          renderLineHighlight: 'all',
          smoothScrolling: true,
          cursorBlinking: 'smooth',
          cursorSmoothCaretAnimation: "on" as const,
        }}
        loading={
          <div className="flex items-center justify-center h-full">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
          </div>
        }
      />
    </div>
  );
};

export default MonacoEditor;