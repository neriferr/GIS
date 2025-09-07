const express = require('express');
const sql = require('mssql');

const app = express();
app.use(express.json());

// 🔧 CONFIGURA AQUÍ TUS DATOS DE SQL SERVER
const dbConfig = {
  user: 'avnadmin',
  password: 'AVNS_-G5oqCrk-xKPUb1iOTg',
  server: 'gis-mysql-gis.d.aivencloud.com',    // o la IP de tu SQL Server
  database: 'defaultdb',
  options: { trustServerCertificate: true }
};

// Endpoint para obtener señales pendientes
app.get('/signals', async (req, res) => {
  try {
    await sql.connect(dbConfig);
    const result = await sql.query`SELECT 
    GISTRNOperacionesForexID   AS id,
    GISTRNOperacionesForexPar  AS symbol,
    GISTRNOperacionesForexTipo_Ope AS side,
    GISTRNOperacionesForexLotaje   AS volume,
    GISTRNOperacionesForexPrecio_E AS entry,
    GISTRNOperacionesForexTake_Pro AS takeProfit,
    GISTRNOperacionesForexStock_Lo AS stopLoss
  FROM GISTRNOperacionesForex
  WHERE GISTRNOperacionesForexEstado = 'ACTIVO'`;
    res.json(result.recordset);
  } catch (err) {
    res.status(500).send(err.message);
  }
});

// ⚡ Puerto dinámico para Render, fallback a 3000 para local
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`✅ API lista en puerto ${PORT}`));
