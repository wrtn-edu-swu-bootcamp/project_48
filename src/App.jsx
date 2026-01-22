import React from 'react';
import Header from './components/Header/Header';
import ChatArea from './components/ChatArea/ChatArea';
import InputArea from './components/InputArea/InputArea';
import Footer from './components/Footer/Footer';
import { useChat } from './hooks/useChat';

function App() {
  const { messages, sendMessage, loading } = useChat();

  return (
    <div className="flex flex-col min-h-screen bg-white">
      {/* Header - 상단 고정 */}
      <Header />
      
      {/* Main Content - 중앙 영역 */}
      <main className="flex-1 overflow-y-auto pb-20 md:pb-24">
        <div className="max-w-3xl mx-auto px-4 py-6">
          <ChatArea 
            messages={messages} 
            loading={loading}
            onQuestionClick={sendMessage}
          />
        </div>
      </main>
      
      {/* Input Area - 하단 고정 */}
      <InputArea onSendMessage={sendMessage} loading={loading} />
      
      {/* Footer */}
      <Footer />
    </div>
  );
}

export default App;
