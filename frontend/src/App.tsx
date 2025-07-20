import React, { useState } from "react";
import {
  AppBar,
  Box,
  CssBaseline,
  Container,
  Tab,
  Tabs,
  Typography,
  Toolbar,
  createTheme,
  ThemeProvider,
} from "@mui/material";
import TableViewer from "./components/TableViewer";
import QueryViewer from "./components/QueryViewer";

const App: React.FC = () => {
  const [tab, setTab] = useState(0);
  const theme = createTheme({
    palette: {
      mode: "light",
      primary: {
        main: "#6a1b9a", // deep purple
      },
      secondary: {
        main: "#ff9800", // orange
      },
    },
    typography: {
      fontFamily: "Roboto, sans-serif",
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="sticky" elevation={1}>
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Montréal Volleyball Club
          </Typography>
          <Tabs
            value={tab}
            onChange={(_, newTab) => setTab(newTab)}
            textColor="inherit"
            indicatorColor="secondary"
            sx={{
              "& .MuiTab-root": {
                fontWeight: "bold",
                fontSize: "1.05rem",
                textTransform: "none",
              },
            }}
          >
            <Tab label="🏠 Home" />
            <Tab label="📋 Tables" />
            <Tab label="📊 Queries" />
          </Tabs>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 5 }}>
        {tab === 0 && (
          <Box textAlign="center" sx={{ py: 8 }}>
            <Typography variant="h3" gutterBottom color="primary">
              Welcome to Montréal Volleyball Club
            </Typography>
            <Typography variant="h6" color="text.secondary" sx={{ mt: 2 }}>
              Explore and manage club data with ease.
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
              Use the tabs above to browse tables and execute predefined
              queries.
            </Typography>
            <Typography
              variant="h4"
              gutterBottom
              color="primary"
              sx={{ mt: 1 }}
            >
              Group: auc353_1
            </Typography>
            <Typography
              variant="body1"
              color="text.secondary"
              sx={{ mt: 1, whiteSpace: "pre-line" }}
            >
              Narendra{"\n"}
              Neelendra{"\n"}
              Nidhi{"\n"}
              Marmik{"\n"}
              Jasmeet
            </Typography>
          </Box>
        )}
        {tab === 1 && <TableViewer />}
        {tab === 2 && <QueryViewer />}
      </Container>
    </ThemeProvider>
  );
};

export default App;
