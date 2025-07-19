import React from 'react';
import { Container, Typography } from '@mui/material';
import TableViewer from './components/TableViewer';
import QueryViewer from './components/QueryViewer';

const App: React.FC = () => {
  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>Montréal Volleyball Club</Typography>
      <TableViewer />
      <QueryViewer />
    </Container>
  );
};

export default App;
