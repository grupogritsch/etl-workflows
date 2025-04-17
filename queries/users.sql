-- Substitua os nomes entre aspas conforme seu caso

-- 1. Criar o usuário com senha
CREATE USER "fabio.pepplow" WITH PASSWORD "Gritsch2@25";

-- 2. Dar permissão para conectar no banco
GRANT CONNECT ON DATABASE raw TO "fabio.pepplow";

-- 3. Dar permissão para acessar o schema (geralmente é "public")
GRANT USAGE ON SCHEMA public TO "fabio.pepplow";

-- 4. Dar permissão de SELECT em todas as tabelas existentes no schema
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "fabio.pepplow";

-- 5. Garantir que o usuário terá SELECT em tabelas futuras também
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO "fabio.pepplow";
