const express = require('express');
const mysql = require('mysql2/promise');

const app = express();
app.use(express.json());

// 📦 Configuración de la conexión a MySQL (usando variables de entorno)
const pool = mysql.createPool({
  host: process.env.DB_HOST,       			// ej: gis-mysql-gis.aivencloud.com
  port: Number(process.env.DB_PORT),        // ej: 15072
  user: process.env.DB_USER,       			// ej: avnadmin
  password: process.env.DB_PASS,   			// tu nueva contraseña
  database: process.env.DB_NAME,
  ssl: {
    ca: fs.readFileSync(path.join(__dirname, 'certs', 'ca.pem'))
  }
});

//	Para verificar si la API falla por MySQL:
pool.getConnection()
  .then(conn => {
    console.log('✅ Conexión MySQL OK');
    conn.release();
  })
  .catch(err => console.error('❌ Error conectando a MySQL:', err));

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
