import React, { useState } from "react";
import api from "../api/client";
import {
  Paper,
  Typography,
  Button,
  Table,
  TableRow,
  TableCell,
  TableHead,
  TableBody,
  Select,
  MenuItem,
} from "@mui/material";

const queryOptions = Array.from({ length: 8 }, (_, i) => i + 1); // [1..8]

const QueryViewer: React.FC = () => {
  const [queryNumber, setQueryNumber] = useState(1);
  const [rows, setRows] = useState<any[]>([]);
  const [columns, setColumns] = useState<string[]>([]);
  const [error, setError] = useState("");

  const runQuery = async () => {
    try {
      const res = await api.get(`/query/${queryNumber}`);
      const data = res.data;
      if (data.length > 0) {
        setColumns(Object.keys(data[0]));
        setRows(data);
      } else {
        setColumns([]);
        setRows([]);
      }
      setError("");
    } catch {
      setError("Invalid query or server error");
    }
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Run Predefined Query (1–8)
      </Typography>
      <Select
        value={queryNumber}
        onChange={(e) => setQueryNumber(Number(e.target.value))}
        sx={{ mr: 2, minWidth: 150 }}
      >
        {queryOptions.map((num) => (
          <MenuItem key={num} value={num}>
            Query {num}
          </MenuItem>
        ))}
      </Select>
      <Button variant="contained" onClick={runQuery}>
        Run
      </Button>
      {error && <Typography color="error">{error}</Typography>}
      {rows.length > 0 && (
        <Paper sx={{ overflow: "auto", maxHeight: 500 }}>
          <Table stickyHeader size="small">
            <TableHead>
              <TableRow>
                {columns.map((col) => (
                  <TableCell key={col}>
                    <strong>{col}</strong>
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map((row, i) => (
                <TableRow key={i}>
                  {columns.map((col) => (
                    <TableCell key={col}>{row[col]}</TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}
    </Paper>
  );
};

export default QueryViewer;
