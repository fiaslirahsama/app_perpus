DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS buku;
DROP TABLE IF EXISTS transaksi;

CREATE TABLE admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    nama TEXT NOT NULL
);

CREATE TABLE member(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idmember TEXT UNIQUE NOT NULL,
    nik VARCHAR NOT NULL,
    nama TEXT NOT NULL,
    jenis_kelamin TEXT NOT NULL,
    alamat TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    created_by VARCHAR NOT NULL,
    updated_at TIMESTAMP,
    updated_by VARCHAR,
    flag VARCHAR NOT NULL DEFAULT 'on'
);

CREATE TABLE buku(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn TEXT UNIQUE NOT NULL,
    judul TEXT NOT NULL,
    genre TEXT NOT NULL,
    sinopsis TEXT NOT NULL,
    status VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    created_by VARCHAR NOT NULL,
    updated_at TIMESTAMP,
    updated_by VARCHAR,
    flag VARCHAR NOT NULL DEFAULT 'on'
);

CREATE TABLE transaksi(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idmember INTEGER NOT NULL,
    isbn INTEGER NOT NULL,
    tgl_pinjam DATE NOT NULL DEFAULT (CURRENT_DATE),
    tgl_kembali DATE NOT NULL,
    idadmin INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP),
    created_by VARCHAR NOT NULL,
    updated_at TIMESTAMP,
    updated_by VARCHAR,
    flag VARCHAR NOT NULL DEFAULT 'on',
    FOREIGN KEY (idmember) REFERENCES member(idmember),
    FOREIGN KEY (isbn) REFERENCES buku(isbn),
    FOREIGN KEY (idadmin) REFERENCES admin(id)
);