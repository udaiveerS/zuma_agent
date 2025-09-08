import React, { useRef, useEffect } from 'react';
import {
  Box,
  List,
  ListItem,
} from '@mui/material';
import { MessageListProps } from '../types/chat';
import MessageItem from './MessageItem';
import TypingIndicator from './TypingIndicator';

const MessageList: React.FC<MessageListProps> = ({ messages }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ 
      behavior: "smooth",
      block: "end"
    });
  };

  // Auto-scroll when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Also scroll when component first mounts
  useEffect(() => {
    scrollToBottom();
  }, []);

  return (
    <Box
      ref={containerRef}
      sx={{
        flex: 1,
        overflow: 'auto',
        p: 1,
        scrollBehavior: 'smooth',
      }}
    >
      <List sx={{ p: 0 }}>
        {messages.map((message) => {
          // Show typing indicator for typing messages
          if (message.id === 'typing-indicator') {
            return (
              <ListItem key={message.id} sx={{ p: 0 }}>
                <TypingIndicator />
              </ListItem>
            );
          }
          return <MessageItem key={message.id} message={message} />;
        })}
        {/* Invisible div to scroll to */}
        <div ref={messagesEndRef} style={{ height: '1px' }} />
      </List>
    </Box>
  );
};

export default MessageList;
