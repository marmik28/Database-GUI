import React, { useState } from 'react';
import api from '../api/client';
import {
  Table, TableHead, TableRow, TableCell, TableBody,
  Paper, Typography, Button, Select, MenuItem
} from '@mui/material';

const tableOptions = [
  'clubmembers',
  'personnel',
  'locations',
  'roles',
  'personnel_location_history',
  'familymembers',
  'familymember_child',
  'member_hobby',
  'hobbies',
  'payments'
];

const TableViewer: React.FC = () => {
  const [tableName, setTableName] = useState('clubmembers');
  const [rows, setRows] = useState<any[]>([]);
  const [columns, setColumns] = useState<string[]>([]);
  const [error, setError] = useState('');

  const fetchTable = async () => {
    try {
      const res = await api.get(`/tables/${tableName}`);
      const data = res.data;
      if (data.length > 0) {
        setColumns(Object.keys(data[0]));
        setRows(data);
      } else {
        setColumns([]);
        setRows([]);
      }
      setError('');
    } catch (err: any) {
      setError('Table not found');
    }
  };

  return (
    <Paper sx={{ p: 3, mb: 4 }}>
      <Typography variant="h6" gutterBottom>Table Viewer</Typography>
      <Select
        value={tableName}
        onChange={(e) => setTableName(e.target.value)}
        sx={{ mr: 2, minWidth: 200 }}
      >
        {tableOptions.map((name) => (
          <MenuItem key={name} value={name}>{name}</MenuItem>
        ))}
      </Select>
      <Button variant="contained" onClick={fetchTable}>View</Button>
      {error && <Typography color="error">{error}</Typography>}
      {rows.length > 0 && (
        <Table sx={{ mt: 2 }}>
          <TableHead>
            <TableRow>
              {columns.map(col => <TableCell key={col}><strong>{col}</strong></TableCell>)}
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row, i) => (
              <TableRow key={i}>
                {columns.map(col => <TableCell key={col}>{row[col]}</TableCell>)}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </Paper>
  );
};

export default TableViewer;
