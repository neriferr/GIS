const express = require('express');
const mysql = require('mysql2/promise');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.json());

// 📦 Configuración de la conexión a MySQL (usando variables de entorno)
const pool = mysql.createPool({
  host: process.env.DB_HOST,           // ej: gis-mysql-gis.d.aivencloud.com
  port: Number(process.env.DB_PORT),   // ej: 15072
  user: process.env.DB_USER,           // ej: avnadmin
  password: process.env.DB_PASS,       // tu contraseña
  database: process.env.DB_NAME,       // ej: defaultdb
  ssl: {
    ca: fs.readFileSync(path.join(__dirname, 'certs', 'ca.pem'))
  }
});

// 🔹 Verificar conexión MySQL al iniciar
pool.getConnection()
  .then(conn => {
    console.log('✅ Conexión MySQL OK');
    conn.release();
  })
  .catch(err => {
    console.error('❌ Error conectando a MySQL:', err.message);
  });

// 🟢 Endpoint para obtener señales activas
app.get('/signals', async (req, res) => {
  try {
    const [rows] = await pool.query(`
      SELECT 
        GISTRNOperacionesForexID   AS id,
        GISTRNOperacionesForexPar  AS symbol,
        GISTRNOperacionesForexTipo_Ope AS side,
        GISTRNOperacionesForexLotaje   AS volume,
        GISTRNOperacionesForexPrecio_E AS entry,
        GISTRNOperacionesForexTake_Pro AS takeProfit,
        GISTRNOperacionesForexStock_Lo AS stopLoss
      FROM GISTRNOperacionesForex
      WHERE GISTRNOperacionesForexEstado = 'ACTIVO'
    `);
    res.json(rows);
  } catch (err) {
    console.error('❌ Error en consulta:', err.message);
    res.status(500).send('Error en el servidor');
  }
});

// 🚀 Puerto dinámico para Render (fallback 3000 en local)
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`✅ API lista en puerto ${PORT}`));
