import React from 'react';
import { Box, Typography, Avatar, keyframes } from '@mui/material';
import { SmartToy } from '@mui/icons-material';
import { grey } from '@mui/material/colors';

const bounce = keyframes`
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-10px);
  }
`;

const TypingIndicator: React.FC = () => {
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'flex-start',
        alignItems: 'flex-start',
        px: 1,
        py: 0.5,
      }}
    >
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
      <Box
        sx={{
          maxWidth: '70%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
        }}
      >
        <Box
          sx={{
            px: 2,
            py: 1,
            borderRadius: 2,
            bgcolor: grey[100],
            color: 'text.primary',
            position: 'relative',
            minWidth: '60px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Typography
            variant="body1"
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 0.5,
            }}
          >
            <Box
              component="span"
              sx={{
                width: 6,
                height: 6,
                borderRadius: '50%',
                bgcolor: 'text.secondary',
                animation: `${bounce} 1.4s infinite ease-in-out`,
                animationDelay: '0s',
              }}
            />
            <Box
              component="span"
              sx={{
                width: 6,
                height: 6,
                borderRadius: '50%',
                bgcolor: 'text.secondary',
                animation: `${bounce} 1.4s infinite ease-in-out`,
                animationDelay: '0.2s',
              }}
            />
            <Box
              component="span"
              sx={{
                width: 6,
                height: 6,
                borderRadius: '50%',
                bgcolor: 'text.secondary',
                animation: `${bounce} 1.4s infinite ease-in-out`,
                animationDelay: '0.4s',
              }}
            />
          </Typography>
        </Box>
        <Typography
          variant="caption"
          sx={{
            color: 'text.secondary',
            mt: 0.5,
            px: 1,
          }}
        >
          AI is typing...
        </Typography>
      </Box>
    </Box>
  );
};

export default TypingIndicator;
