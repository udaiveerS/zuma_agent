import React from 'react';
import {
  Box,
  Typography,
  Stack,
  Avatar,
} from '@mui/material';
import { SmartToy } from '@mui/icons-material';
import { ChatHeaderProps } from '../types/chat';

const ChatHeader: React.FC<ChatHeaderProps> = ({
  title = "AI Assistant Chat",
  subtitle = "Ask me anything! I'm here to help with questions and conversations."
}) => {
  return (
    <Box
      sx={{
        p: 2,
        borderBottom: 1,
        borderColor: 'divider',
        bgcolor: 'background.paper',
      }}
    >
      <Stack direction="row" alignItems="center" spacing={2}>
        <Avatar
          sx={{
            bgcolor: 'primary.main',
            width: 40,
            height: 40,
          }}
        >
          <SmartToy />
        </Avatar>
        <Box>
          <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.5 }}>
            {title}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {subtitle}
          </Typography>
        </Box>
      </Stack>
    </Box>
  );
};

export default ChatHeader;
