import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '@/store';
import { openFile, closeTab, setActiveTab, saveFile } from '@/store/slices/editorSlice';
import { setSidebarPanel } from '@/store/slices/uiSlice';
import MonacoEditor from '@/components/Editor/MonacoEditor';
import { EditorFile } from '@/types';
import { 
  XMarkIcon, 
  PlusIcon, 
  DocumentIcon,
  FolderIcon,
  CodeBracketIcon,
  CloudArrowUpIcon,
  ExclamationCircleIcon
} from '@heroicons/react/24/outline';
import { classNames } from '@/utils';

const Editor: React.FC = () => {
  const dispatch = useDispatch();
  const { files, tabs, activeTabId } = useSelector((state: RootState) => state.editor);
  const { sidebar } = useSelector((state: RootState) => state.ui);
  const [isFileTreeOpen, setIsFileTreeOpen] = useState(true);

  useEffect(() => {
    // Ensure sidebar is open and showing files
    if (sidebar.activePanel !== 'files') {
      dispatch(setSidebarPanel('files'));
    }
  }, [dispatch, sidebar.activePanel]);

  const activeTab = tabs.find(tab => tab.id === activeTabId);
  const activeFile = activeTab ? files.find(file => file.id === activeTab.file_id) : null;

  const handleTabClick = (tabId: string) => {
    dispatch(setActiveTab(tabId));
  };

  const handleTabClose = (tabId: string, event: React.MouseEvent) => {
    event.stopPropagation();
    dispatch(closeTab(tabId));
  };

  const handleNewFile = () => {
    const newFile: EditorFile = {
      id: `file-${Date.now()}`,
      name: 'untitled.js',
      path: '/untitled.js',
      content: '// Welcome to OmniDev Supreme!\n// Start coding with AI-powered assistance\n\nconsole.log("Hello, OmniDev Supreme!");',
      language: 'javascript',
      is_dirty: false,
    };
    dispatch(openFile(newFile));
  };

  const handleSaveFile = async (fileId: string) => {
    const file = files.find(f => f.id === fileId);
    if (file) {
      try {
        await dispatch(saveFile({ fileId, content: file.content }) as any);
      } catch (error) {
        console.error('Failed to save file:', error);
      }
    }
  };

  const handleContentChange = (_content: string) => {
    // Content change is handled by the Monaco Editor component
    // via the updateFileContent action
  };

  return (
    <div className="flex h-full bg-gray-900">
      {/* File Explorer (if no sidebar or sidebar is not showing files) */}
      {(!sidebar.isOpen || sidebar.activePanel !== 'files') && (
        <div className="w-64 bg-gray-800 border-r border-gray-600 flex flex-col">
          <div className="p-4 border-b border-gray-600">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-white">Files</h2>
              <button
                onClick={() => setIsFileTreeOpen(!isFileTreeOpen)}
                className="text-gray-400 hover:text-white"
              >
                <FolderIcon className="w-5 h-5" />
              </button>
            </div>
            
            <button
              onClick={handleNewFile}
              className="w-full flex items-center space-x-2 px-3 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
            >
              <PlusIcon className="w-4 h-4" />
              <span>New File</span>
            </button>
          </div>

          {isFileTreeOpen && (
            <div className="flex-1 overflow-y-auto p-4">
              <div className="space-y-2">
                {files.map(file => (
                  <div
                    key={file.id}
                    className={classNames(
                      'flex items-center space-x-2 px-3 py-2 rounded-md cursor-pointer transition-colors',
                      activeFile?.id === file.id 
                        ? 'bg-primary-600 text-white' 
                        : 'text-gray-300 hover:bg-gray-700'
                    )}
                    onClick={() => dispatch(openFile(file))}
                  >
                    <DocumentIcon className="w-4 h-4" />
                    <span className="flex-1 truncate">{file.name}</span>
                    {file.is_dirty && (
                      <div className="w-2 h-2 bg-warning-500 rounded-full"></div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Editor Area */}
      <div className="flex-1 flex flex-col">
        {/* Tab Bar */}
        <div className="flex items-center bg-gray-800 border-b border-gray-600 overflow-x-auto">
          {tabs.map(tab => (
            <div
              key={tab.id}
              className={classNames(
                'flex items-center space-x-2 px-4 py-2 border-r border-gray-600 cursor-pointer group min-w-0',
                tab.is_active 
                  ? 'bg-gray-900 text-white' 
                  : 'text-gray-300 hover:bg-gray-700'
              )}
              onClick={() => handleTabClick(tab.id)}
            >
              <CodeBracketIcon className="w-4 h-4 flex-shrink-0" />
              <span className="truncate">{tab.name}</span>
              {tab.is_dirty && (
                <div className="w-2 h-2 bg-warning-500 rounded-full flex-shrink-0"></div>
              )}
              <button
                onClick={(e) => handleTabClose(tab.id, e)}
                className="opacity-0 group-hover:opacity-100 hover:bg-gray-600 rounded p-1 transition-all"
              >
                <XMarkIcon className="w-3 h-3" />
              </button>
            </div>
          ))}
          
          <button
            onClick={handleNewFile}
            className="flex items-center space-x-1 px-3 py-2 text-gray-400 hover:text-white hover:bg-gray-700 transition-colors"
          >
            <PlusIcon className="w-4 h-4" />
          </button>
        </div>

        {/* Editor Content */}
        <div className="flex-1 relative">
          {activeFile ? (
            <div className="h-full">
              <MonacoEditor
                fileId={activeFile.id}
                content={activeFile.content}
                language={activeFile.language}
                onContentChange={handleContentChange}
              />
              
              {/* Status Bar */}
              <div className="absolute bottom-0 left-0 right-0 bg-gray-800 border-t border-gray-600 px-4 py-2 flex items-center justify-between text-sm">
                <div className="flex items-center space-x-4">
                  <span className="text-gray-400">
                    {activeFile.language.toUpperCase()}
                  </span>
                  <span className="text-gray-400">
                    {activeFile.cursor_position 
                      ? `Line ${activeFile.cursor_position.line}, Column ${activeFile.cursor_position.column}`
                      : 'Ready'
                    }
                  </span>
                </div>
                
                <div className="flex items-center space-x-2">
                  {activeFile.is_dirty && (
                    <div className="flex items-center space-x-1 text-warning-400">
                      <ExclamationCircleIcon className="w-4 h-4" />
                      <span>Unsaved changes</span>
                    </div>
                  )}
                  
                  <button
                    onClick={() => handleSaveFile(activeFile.id)}
                    className="flex items-center space-x-1 px-2 py-1 bg-primary-600 text-white rounded hover:bg-primary-700 transition-colors"
                  >
                    <CloudArrowUpIcon className="w-4 h-4" />
                    <span>Save</span>
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="h-full flex items-center justify-center text-gray-400">
              <div className="text-center">
                <CodeBracketIcon className="w-16 h-16 mx-auto mb-4" />
                <h3 className="text-lg font-medium mb-2">Welcome to OmniDev Supreme</h3>
                <p className="mb-4">The unified AI development platform with Monaco Editor</p>
                <button
                  onClick={handleNewFile}
                  className="btn btn-primary"
                >
                  Create New File
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Editor;