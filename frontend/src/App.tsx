import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Box,
  CircularProgress,
  Typography,
} from '@mui/material';
import { ChatHeader, ChatInput, MessageList } from './components';
import { Message } from './types/chat';
import { postReply, getMessages } from './api';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);

  // Load messages on app startup
  useEffect(() => {
    const loadInitialMessages = async () => {
      try {
        const response = await getMessages(100); // Get last 100 messages
        setMessages(response.messages || []);
        console.log(`Loaded ${response.messages?.length || 0} messages from backend`);
      } catch (error) {
        console.error('Failed to load chat history:', error);
        // App still works with empty message history
      } finally {
        setIsLoadingHistory(false);
      }
    };

    loadInitialMessages();
  }, []); // Empty dependency array = runs once on mount

  const handleSubmit = async (message: string) => {
    const userMessage: Message = {
      id: `temp-${Date.now()}`, // Temporary ID for optimistic update
      message: {
        role: "user",
        content: message,
      },
      created_date: new Date().toISOString(),
    };

    // Optimistically add user message
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    // Add typing indicator
    const typingMessage: Message = {
      id: 'typing-indicator',
      message: {
        role: "assistant",
        content: "Typing...",
      },
      created_date: new Date().toISOString(),
    };
    
    setMessages(prev => [...prev, typingMessage]);

    try {
      // Call API with just the message string
      const response = await postReply(message);

      // Remove typing indicator and add real response
      setMessages(prev => {
        // Remove the temporary user message and typing indicator
        const withoutTempAndTyping = prev.filter(msg => 
          msg.id !== userMessage.id && msg.id !== 'typing-indicator'
        );
        
        // Convert new response format to Message format for display
        const assistantMessage: Message = {
          id: response.id,
          message: {
            role: "assistant",
            content: response.reply
          },
          created_date: response.created_date,
          action: response.action,
          propose_time: response.propose_time
        };
        
        // Add both the real user message and assistant response
        return [...withoutTempAndTyping, userMessage, assistantMessage];
      });
    } catch (error) {
      console.error('Failed to get response:', error);
      // Remove the optimistic user message and typing indicator on error
      setMessages(prev => prev.filter(msg => 
        msg.id !== userMessage.id && msg.id !== 'typing-indicator'
      ));
      // Optionally show error message
    } finally {
      setIsLoading(false);
    }
  };

  // Show loading screen while fetching initial messages
  if (isLoadingHistory) {
    return (
      <Container maxWidth="sm" sx={{ height: '100vh', py: 2 }}>
        <Paper
          elevation={2}
          sx={{
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            borderRadius: 2,
            bgcolor: 'white',
          }}
        >
          <CircularProgress size={40} sx={{ mb: 2 }} />
          <Typography variant="body1" color="text.secondary">
            Loading chat history...
          </Typography>
        </Paper>
      </Container>
    );
  }

  return (
    <Container maxWidth="sm" sx={{ height: '100vh', py: 2 }}>
      <Paper
        elevation={2}
        sx={{
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          borderRadius: 2,
          bgcolor: 'white',
        }}
      >
        <ChatHeader />
        <MessageList messages={messages} />
        <ChatInput
          value={inputValue}
          onChange={setInputValue}
          onSubmit={handleSubmit}
          isLoading={isLoading}
        />
      </Paper>
    </Container>
  );
}

export default App;
