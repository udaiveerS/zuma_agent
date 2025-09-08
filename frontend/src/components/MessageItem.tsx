import React from 'react';
import {
  ListItem,
  Box,
  Typography,
  Avatar,
  Button,
} from '@mui/material';
import { grey } from '@mui/material/colors';
import { Person, SmartToy, Schedule } from '@mui/icons-material';
import { MessageItemProps } from '../types/chat';

const MessageItem: React.FC<MessageItemProps> = ({ message }) => {
  const isUser = message.message.role === 'user';
  const timestamp = new Date(message.created_date).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  });

  const handleTourConfirmation = () => {
    if (message.propose_time) {
      const tourDate = new Date(message.propose_time);
      const formattedTime = tourDate.toLocaleString([], {
        weekday: 'long',
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
      alert(`Tour confirmed for ${formattedTime}! We'll send you a confirmation email shortly.`);
    }
  };

  const handleTourDenial = () => {
    alert('No problem! Feel free to ask about other available times or if you have any other questions.');
  };

  return (
    <ListItem
      sx={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        alignItems: 'flex-start',
        px: 1,
        py: 0.5,
      }}
    >
      {/* Avatar - only show on left for assistant */}
      {!isUser && (
        <Avatar
          sx={{
            width: 32,
            height: 32,
            bgcolor: 'secondary.main',
            mr: 1,
            mt: 0.5,
          }}
        >
          <SmartToy fontSize="small" />
        </Avatar>
      )}
      
      {/* Message Content */}
      <Box
        sx={{
          maxWidth: '70%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: isUser ? 'flex-end' : 'flex-start',
        }}
      >
        {/* Message Bubble */}
        <Box
          sx={{
            px: 2,
            py: 1,
            borderRadius: 2,
            bgcolor: isUser ? 'primary.main' : grey[100],
            color: isUser ? 'white' : 'text.primary',
            position: 'relative',
          }}
        >
          <Typography variant="body1">
            {message.message.content}
          </Typography>
        </Box>
        
        {/* Tour Confirmation Buttons */}
        {!isUser && message.action === 'propose_tour' && message.propose_time && (
          <Box sx={{ mt: 1, display: 'flex', gap: 1, flexDirection: 'column' }}>
            {/* Tour Time Display */}
            <Typography variant="body2" sx={{ color: 'text.secondary', fontWeight: 'medium' }}>
              {(() => {
                const tourDate = new Date(message.propose_time);
                const time = tourDate.toLocaleTimeString([], { 
                  hour: 'numeric', 
                  minute: '2-digit',
                  hour12: true 
                });
                const day = tourDate.toLocaleDateString([], { 
                  weekday: 'long',
                  month: 'short', 
                  day: 'numeric' 
                });
                return `Proposed tour: ${day} at ${time}`;
              })()}
            </Typography>
            
            {/* Confirm/Deny Buttons */}
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button
                variant="contained"
                color="primary"
                size="small"
                onClick={handleTourConfirmation}
                sx={{
                  borderRadius: 2,
                  textTransform: 'none',
                  fontWeight: 'medium',
                  flex: 1,
                }}
              >
                Confirm Tour
              </Button>
              <Button
                variant="outlined"
                color="primary"
                size="small"
                onClick={handleTourDenial}
                sx={{
                  borderRadius: 2,
                  textTransform: 'none',
                  fontWeight: 'medium',
                  flex: 1,
                }}
              >
                Not Available
              </Button>
            </Box>
          </Box>
        )}
        
        {/* Timestamp */}
        <Typography 
          variant="caption" 
          sx={{ 
            color: 'text.secondary',
            mt: 0.5,
            px: 1,
          }}
        >
          {timestamp}
        </Typography>
      </Box>
      
      {/* Avatar - only show on right for user */}
      {isUser && (
        <Avatar
          sx={{
            width: 32,
            height: 32,
            bgcolor: 'primary.main',
            ml: 1,
            mt: 0.5,
          }}
        >
          <Person fontSize="small" />
        </Avatar>
      )}
    </ListItem>
  );
};

export default MessageItem;
