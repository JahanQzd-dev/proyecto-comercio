<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>README — PROYECTO COMERCIO</title>
  <style>
    :root{--bg:#0f1724;--card:#0b1220;--muted:#9aa4b2;--accent:#60a5fa;--glass: rgba(255,255,255,0.03)}
    html,body{height:100%;margin:0;font-family:Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; background: linear-gradient(180deg,#071029 0%, #071427 100%); color:#e6eef6}
    .wrap{max-width:980px;margin:36px auto;padding:28px;background:linear-gradient(180deg,var(--card), rgba(11,18,32,0.9));border-radius:14px;box-shadow:0 10px 30px rgba(2,6,23,0.6);border:1px solid rgba(255,255,255,0.03)}
    header{display:flex;align-items:center;gap:16px;margin-bottom:18px}
    .logo{width:64px;height:64px;border-radius:12px;background:linear-gradient(135deg,var(--accent),#3b82f6);display:flex;align-items:center;justify-content:center;font-weight:700;color:#071127}
    h1{margin:0;font-size:22px}
    p.lead{margin:6px 0 0;color:var(--muted)}
    section{margin-top:18px;padding-top:12px;border-top:1px dashed rgba(255,255,255,0.02)}
    h2{font-size:16px;margin:0 0 10px}
    pre{background:var(--glass);padding:12px;border-radius:8px;overflow:auto;border:1px solid rgba(255,255,255,0.02);margin:0}
    code{font-family:SFMono-Regular, Menlo, Monaco, 'Courier New', monospace;font-size:13px;color:#dbeafe}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
    .full{grid-column:1/-1}
    .btn{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border-radius:8px;border:0;background:linear-gradient(90deg,#1e293b,#0f1724);color:#e6eef6;cursor:pointer}
    .muted{color:var(--muted);font-size:13px}
    .badge{display:inline-block;padding:6px 10px;border-radius:999px;background:rgba(255,255,255,0.04);font-size:13px}
    .note{background:linear-gradient(90deg, rgba(96,165,250,0.07), rgba(59,130,246,0.04));padding:10px;border-radius:8px;border:1px solid rgba(96,165,250,0.08);color:#cfe8ff}
    footer{margin-top:18px;color:var(--muted);font-size:13px}
    .copy{float:right}
    @media (max-width:720px){.grid{grid-template-columns:1fr}.logo{width:52px;height:52px}}
  </style>
</head>
<body>
  <div class="wrap" role="main">
    <header>
      <div class="logo">PC</div>
      <div>
        <h1>PROYECTO COMERCIO</h1>
        <p class="lead">API backend desarrollada con <strong>Flask</strong> y <strong>SQLite</strong>, creada como proyecto para aprender los fundamentos del desarrollo backend, rutas, modelos, y manejo básico de una base de datos ligera.</p>
      </div>
    </header>

    <section>
      <h2>📦 Descripción del proyecto</h2>
      <p>proyecto-comercio es una API sencilla diseñada para simular la lógica de un pequeño sistema de comercio. Incluye estructuras básicas para manejar recursos (usuarios, clientes, productos, compras, etc.) y sirve como base para futuros proyectos más completos.</p>
    </section>

    <section class="grid">
      <div>
        <h2>🛠️ Tecnologías utilizadas</h2>
        <ul class="muted">
          <li>Python 3</li>
          <li>Flask</li>
          <li>Flask-RESTful</li>
          <li>SQLite</li>
          <li>Flask SQLAlchemy</li>
        </ul>
      </div>
      <div>
        <h2>🧩 Objetivo del proyecto</h2>
        <ul class="muted">
          <li>Practicar CRUDs</li>
          <li>Entender cómo funciona Flask por dentro</li>
          <li>Aprender a estructurar APIs</li>
          <li>Manejar una base de datos con SQLAlchemy + SQLite</li>
          <li>Subir y versionar un proyecto en GitHub</li>
        </ul>
      </div>

      <div class="full">
        <h2>🔧 Configuración de variables de entorno</h2>
        <p class="muted">Este proyecto utiliza variables de entorno para manejar información sensible (puertos, claves, credenciales de correo, etc.). En el repositorio se incluye un archivo <code>.env-example</code> con la estructura necesaria. Antes de ejecutar la aplicación, se debe crear un archivo <code>.env</code> propio basado en este ejemplo.</p>

        <div class="note">
          <strong>Importante:</strong> No subas tu archivo <code>.env</code> al repositorio. Mantén tus claves y credenciales privadas.
        </div>

        <h3 style="margin-top:10px">Ejemplo — .env-example</h3>
        <pre id="env-example"><code># CONFIGURAR CADA UNA DE LAS VARIABLES

# App flask
export PORT=0000

# Db config
export DATABASE_NAME='nombre.db'
export DATABASE_PATH='PATH/ABSOLUTO/'

# JWT config
export JWT_SECRET_KEY='clave'
export JWT_ACCESS_TOKEN_EXPIRES=3600

# Mail config
export MAIL_SERVER='smtp.gmail.com'
export MAIL_PORT='587'
export MAIL_USE_TLS='True'
export MAIL_USERNAME='mail@gmail.com'
export MAIL_PASSWORD='clavedelmail'
export FLASKY_MAIL_SENDER='App <admin@app.com>'</code></pre>

        <div style="margin-top:10px" class="muted">Sugerencias:
          <ul>
            <li>Usa rutas absolutas reales en <code>DATABASE_PATH</code>.</li>
            <li>Revisa que <code>MAIL_USERNAME</code> y <code>MAIL_PASSWORD</code> pertenezcan a una cuenta autorizada para envío SMTP.</li>
            <li>Evita comillas innecesarias en valores numéricos.</li>
          </ul>
        </div>

      </div>
    </section>

    <footer>
      <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap">
        <div class="muted">Licencia: uso educativo y personal</div>
        <div class="badge">No subir <code>.env</code></div>
      </div>
    </footer>
  </div>

  <script>
    function copyText(id){
      const el = document.getElementById(id) || document.querySelector('#'+id+' code') || document.querySelector('pre code');
      const text = el ? el.innerText : '';
      if(!text) return alert('Nada para copiar');
      navigator.clipboard.writeText(text).then(()=>{
        const old = document.title;
        document.title = 'Copiado ✅';
        setTimeout(()=>document.title = old,1200);
      }).catch(()=>alert('No se pudo copiar.'));
    }
  </script>
</body>
</html>
