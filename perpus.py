from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for, make_response
)
import os
from os.path import join, dirname, realpath
from werkzeug.exceptions import abort
import time, datetime
from flaskbooknew.auth import login_required
from flaskbooknew.db import get_db
from io import StringIO
import csv
from flaskbooknew import app

bp = Blueprint('perpus', __name__)

##################################### index #################################
@bp.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    transaksi = searchtransaksi()[0]
    cp = searchtransaksi()[1]
    cj = searchtransaksi()[2]
    cw1 = searchtransaksi()[3]
    cw2 = searchtransaksi()[4]

    return render_template('perpus/index.html', transaksi=transaksi, cp=cp, cj=cj, cw1=cw1, cw2=cw2)

def searchtransaksi():
    db = get_db()
    cp = cj = cw1 = cw2 = ''
    transaksi = db.execute(
        'SELECT * FROM(SELECT  transaksi.id, member.nama, buku.judul, tgl_pinjam, tgl_kembali, admin.nama AS namaadmin, transaksi.flag'
        ' FROM transaksi '
        ' JOIN member ON transaksi.idmember = member.idmember'
        ' JOIN buku ON transaksi.isbn = buku.isbn'
        ' JOIN admin ON transaksi.idadmin = admin.id'
        ' WHERE transaksi.flag = "on" ORDER BY tgl_pinjam DESC)'
    ).fetchall()
    
    if request.method == 'POST': #search data berdasarkan input = 4 jenis, Logika Searching 2^input = 16
        if 'caridatatransaksi' in request.form:
            caripeminjam = cp = request.form['caripeminjam']
            carijudul = cj = request.form['carijudul']
            cariwaktu1 = cw1 = request.form['cariwaktu1']
            cariwaktu2 = cw2 = request.form['cariwaktu2']

            if not cw1 and not cw2:
                cp = cj = p = "%"
                cp += str(caripeminjam)
                cp += p
                cj += str(carijudul)
                cj += p
                transaksi = transaksi = db.execute(
                    'SELECT * FROM(SELECT  transaksi.id, member.nama, buku.judul, tgl_pinjam, tgl_kembali, admin.nama AS namaadmin, transaksi.flag'
                    ' FROM transaksi '
                    ' JOIN member ON transaksi.idmember = member.idmember'
                    ' JOIN buku ON transaksi.isbn = buku.isbn'
                    ' JOIN admin ON transaksi.idadmin = admin.id'
                    ' WHERE transaksi.flag = "on" ORDER BY tgl_pinjam DESC)'
                    ' WHERE nama LIKE ? AND judul LIKE ?',
                (cp,cj,)).fetchall()
            elif not cw1 and cw2:
                cp = cj = p = "%"
                cp += str(caripeminjam)
                cp += p
                cj += str(carijudul)
                cj += p
                transaksi = transaksi = db.execute(
                    'SELECT * FROM(SELECT  transaksi.id, member.nama, buku.judul, tgl_pinjam, tgl_kembali, admin.nama AS namaadmin, transaksi.flag'
                    ' FROM transaksi '
                    ' JOIN member ON transaksi.idmember = member.idmember'
                    ' JOIN buku ON transaksi.isbn = buku.isbn'
                    ' JOIN admin ON transaksi.idadmin = admin.id'
                    ' WHERE transaksi.flag = "on" ORDER BY tgl_pinjam DESC)'
                    ' WHERE nama LIKE ? AND judul LIKE ? AND tgl_kembali <= date(?)',
                (cp,cj,cw2)).fetchall()
            elif cw1 and not cw2:
                cp = cj = p = "%"
                cp += str(caripeminjam)
                cp += p
                cj += str(carijudul)
                cj += p
                transaksi = transaksi = db.execute(
                    'SELECT * FROM(SELECT  transaksi.id, member.nama, buku.judul, tgl_pinjam, tgl_kembali, admin.nama AS namaadmin, transaksi.flag'
                    ' FROM transaksi '
                    ' JOIN member ON transaksi.idmember = member.idmember'
                    ' JOIN buku ON transaksi.isbn = buku.isbn'
                    ' JOIN admin ON transaksi.idadmin = admin.id'
                    ' WHERE transaksi.flag = "on" ORDER BY tgl_pinjam DESC)'
                    ' WHERE nama LIKE ? AND judul LIKE ? AND tgl_kembali >= date(?)',
                (cp,cj,cw1)).fetchall()
            elif cw1 and cw2:
                cp = cj = p = "%"
                cp += str(caripeminjam)
                cp += p
                cj += str(carijudul)
                cj += p
                transaksi = transaksi = db.execute(
                    'SELECT * FROM(SELECT  transaksi.id, member.nama, buku.judul, tgl_pinjam, tgl_kembali, admin.nama AS namaadmin, transaksi.flag'
                    ' FROM transaksi '
                    ' JOIN member ON transaksi.idmember = member.idmember'
                    ' JOIN buku ON transaksi.isbn = buku.isbn'
                    ' JOIN admin ON transaksi.idadmin = admin.id'
                    ' WHERE transaksi.flag = "on" ORDER BY tgl_pinjam DESC)'
                    ' WHERE nama LIKE ? AND judul LIKE ? AND tgl_kembali BETWEEN date(?) AND date(?)',
                (cp,cj,cw1,cw2)).fetchall()
                
    return transaksi, cp, cj, cw1, cw2

#############################################################################
@bp.route('/downloadtransaksi', methods=('GET','POST'))
@login_required
def downloadtransaksi():
    db = get_db()
    cp = cj = cw1 = cw2 = ''
    transaksi = db.execute(
        'SELECT nama,judul,tgl_pinjam,tgl_kembali,namaadmin FROM(SELECT  transaksi.id, member.nama, buku.judul, tgl_pinjam, tgl_kembali, admin.nama AS namaadmin, transaksi.flag'
        ' FROM transaksi '
        ' JOIN member ON transaksi.idmember = member.idmember'
        ' JOIN buku ON transaksi.isbn = buku.isbn'
        ' JOIN admin ON transaksi.idadmin = admin.id'
        ' WHERE transaksi.flag = "on" ORDER BY tgl_pinjam DESC)'
    ).fetchall()
    
    if request.method == 'POST': #search data 
        if 'downloaddatatransaksi' in request.form:
            caripeminjam = cp = request.form['cp']
            carijudul = cj = request.form['cj']
            cariwaktu1 = cw1 = request.form['cw1']
            cariwaktu2 = cw2 = request.form['cw2']
            if cw1 == 'None':
                cw1 = ''
            elif cw2 == 'None':
                cw2 = ''

            if not cw1 and not cw2:
                cp = cj = p = "%"
                cp += str(caripeminjam)
                cp += p
                cj += str(carijudul)
                cj += p
                transaksi = transaksi = db.execute(
                    'SELECT nama,judul,tgl_pinjam,tgl_kembali,namaadmin FROM(SELECT  transaksi.id, member.nama, buku.judul, tgl_pinjam, tgl_kembali, admin.nama AS namaadmin, transaksi.flag'
                    ' FROM transaksi '
                    ' JOIN member ON transaksi.idmember = member.idmember'
                    ' JOIN buku ON transaksi.isbn = buku.isbn'
                    ' JOIN admin ON transaksi.idadmin = admin.id'
                    ' WHERE transaksi.flag = "on" ORDER BY tgl_pinjam DESC)'
                    ' WHERE nama LIKE ? AND judul LIKE ?',
                (cp,cj,)).fetchall()
            elif not cw1 and cw2:
                cp = cj = p = "%"
                cp += str(caripeminjam)
                cp += p
                cj += str(carijudul)
                cj += p
                transaksi = transaksi = db.execute(
                    'SELECT nama,judul,tgl_pinjam,tgl_kembali,namaadmin FROM(SELECT  transaksi.id, member.nama, buku.judul, tgl_pinjam, tgl_kembali, admin.nama AS namaadmin, transaksi.flag'
                    ' FROM transaksi '
                    ' JOIN member ON transaksi.idmember = member.idmember'
                    ' JOIN buku ON transaksi.isbn = buku.isbn'
                    ' JOIN admin ON transaksi.idadmin = admin.id'
                    ' WHERE transaksi.flag = "on" ORDER BY tgl_pinjam DESC)'
                    ' WHERE nama LIKE ? AND judul LIKE ? AND tgl_kembali <= date(?)',
                (cp,cj,cw2)).fetchall()
            elif cw1 and not cw2:
                cp = cj = p = "%"
                cp += str(caripeminjam)
                cp += p
                cj += str(carijudul)
                cj += p
                transaksi = transaksi = db.execute(
                    'SELECT nama,judul,tgl_pinjam,tgl_kembali,namaadmin FROM(SELECT  transaksi.id, member.nama, buku.judul, tgl_pinjam, tgl_kembali, admin.nama AS namaadmin, transaksi.flag'
                    ' FROM transaksi '
                    ' JOIN member ON transaksi.idmember = member.idmember'
                    ' JOIN buku ON transaksi.isbn = buku.isbn'
                    ' JOIN admin ON transaksi.idadmin = admin.id'
                    ' WHERE transaksi.flag = "on" ORDER BY tgl_pinjam DESC)'
                    ' WHERE nama LIKE ? AND judul LIKE ? AND tgl_kembali >= date(?)',
                (cp,cj,cw1)).fetchall()
            elif cw1 and cw2:
                cp = cj = p = "%"
                cp += str(caripeminjam)
                cp += p
                cj += str(carijudul)
                cj += p
                transaksi = transaksi = db.execute(
                    'SELECT nama,judul,tgl_pinjam,tgl_kembali,namaadmin FROM(SELECT  transaksi.id, member.nama, buku.judul, tgl_pinjam, tgl_kembali, admin.nama AS namaadmin, transaksi.flag'
                    ' FROM transaksi '
                    ' JOIN member ON transaksi.idmember = member.idmember'
                    ' JOIN buku ON transaksi.isbn = buku.isbn'
                    ' JOIN admin ON transaksi.idadmin = admin.id'
                    ' WHERE transaksi.flag = "on" ORDER BY tgl_pinjam DESC)'
                    ' WHERE nama LIKE ? AND judul LIKE ? AND tgl_kembali BETWEEN date(?) AND date(?)',
                (cp,cj,cw1,cw2)).fetchall()

    export_transaksi = ['Nama', 'Judul', 'Tanggal Pinjam', 'Tanggal Kembali', 'Nama Admin']
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(export_transaksi)
    cw.writerows(transaksi)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=datatransaksi.csv"
    output.headers["Content-type"] = "text/csv"
    print(cp,cj,cw1,cw2)
    return output
##################################### BUKU ###################################
@bp.route('/tambahbuku', methods=('GET', 'POST'))
@login_required
def tambahbuku(): #### Fungsi Penambahan Buku ####
    db = get_db()
    buku = searchbuku()[0]
    tes = searchbuku()[1]
    ci = searchbuku()[2]
    cj = searchbuku()[3]
    cg = searchbuku()[4]
    cp = searchbuku()[5]
    ca = searchbuku()[6]
    if request.method == 'POST':
        if 'tambahbuku' in request.form:
            isbn = request.form['isbn']
            judul = request.form['judul']
            genre = request.form['genre']
            sinopsis = request.form['sinopsis']
            status = request.form['status']
            databuku = db.execute('SELECT isbn FROM buku WHERE isbn = ? ', (isbn,)).fetchone()
            error = None

            if not isbn:
                error = 'masukkan kode isbn'
            elif not judul:
                error = 'masukkan judul'
            elif not genre:
                error = 'masukkan genre'
            elif not sinopsis:
                error = 'tulis sinopsisnya'
            elif databuku is not None:
                error = 'isbn sudah terpakai'
            
            
            if error is None:
                db.execute(
                    'INSERT INTO buku (isbn, judul, genre, sinopsis, status, created_by)'
                    ' VALUES (?, ?, ?, ?, ?, ?)', (isbn, judul, genre, sinopsis, status, g.admin['nama'],)
                )
                db.commit()
                db.close()
                return redirect(url_for('perpus.tambahbuku'))

            flash(error)
    return render_template('perpus/tambahbuku.html', buku=buku, tes=tes, ci=ci, cj=cj, cg=cg, cp=cp, ca=ca)

def searchbuku(): #### Fungsi Pencarian Buku ####
    db = get_db()
    ci = cj = cg = cp = ca = tes = ''
    buku = db.execute('SELECT id,isbn,judul,genre,sinopsis,status FROM buku WHERE status = "ada" AND flag = "on"').fetchall()
    
    if request.method == 'POST': #search data berdasarkan input = 5 jenis, Logika Searching 2^input = 32
        
        if 'caridatabuku' in request.form:
            
            cariisbn  = ci = request.form['cariisbn']
            carijudul = cj = request.form['carijudul']
            carigenre = cg = request.form['carigenre']
            caripinjam = cp = request.form.get('caripinjam')
            cariada = ca = request.form.get('cariada')

            ci = cj = cg = p = "%"
            ci += str(cariisbn)
            ci += p
            cj += str(carijudul)
            cj += p
            cg += str(carigenre)
            cg += p

            if not cp and not ca:
                buku = db.execute('SELECT id,isbn,judul,genre,sinopsis,status FROM buku WHERE isbn LIKE ? AND judul LIKE ? AND genre LIKE ? '
                 ' AND flag = "on"',(ci, cj, cg,)).fetchall()
            elif not cp and ca:
                buku = db.execute('SELECT id,isbn,judul,genre,sinopsis,status FROM buku WHERE isbn LIKE ? AND judul LIKE ? AND genre LIKE ? '
                 ' AND status = ? AND flag = "on"',(ci, cj, cg, ca,)).fetchall()
            elif cp and not ca:
                buku = db.execute('SELECT id,isbn,judul,genre,sinopsis,status FROM buku WHERE isbn LIKE ? AND judul LIKE ? AND genre LIKE ? '
                 ' AND status = ? AND flag = "on"',(ci, cj, cg, cp,)).fetchall()
            elif cp and ca:
                buku = db.execute('SELECT id,isbn,judul,genre,sinopsis,status FROM buku WHERE isbn LIKE ? AND judul LIKE ? AND genre LIKE ? '
                 ' AND flag = "on"',(ci, cj, cg,)).fetchall()

    return buku,tes,ci,cj,cg,cp,ca

@bp.route('/downloadbuku', methods=('GET','POST'))
@login_required
def downloadbuku():
    db = get_db()
    ci = cj = cg = cp = ca = ''
    buku = db.execute('SELECT isbn,judul,genre,sinopsis,status FROM buku WHERE status = "ada" AND flag = "on"').fetchall()
    if request.method == 'POST':

        if 'downloaddatabuku' in request.form:

            cariisbn  = ci = request.form['ci']
            carijudul = cj = request.form['cj']
            carigenre = cg = request.form['cg']
            caripinjam = cp = request.form.get('cp')
            cariada = ca = request.form.get('ca')

            if cp == 'None' and ca == 'None':
                print("cp:",cp,"ca:",ca)
                cp = ca = ''
            elif cp == 'None' and ca == 'ada':
                print("cp:",cp,"ca:",ca)
                cp = ''
            elif cp == 'dipinjam' and ca == 'None':
                print("cp:",cp,"ca:",ca)
                ca = ''

            ci = cj = cg = p = "%"
            ci += str(cariisbn)
            ci += p
            cj += str(carijudul)
            cj += p
            cg += str(carigenre)
            cg += p

            if not cp and not ca:
                buku = db.execute('SELECT isbn,judul,genre,sinopsis,status FROM buku WHERE isbn LIKE ? AND judul LIKE ? AND genre LIKE ? '
                ' AND flag = "on"',(ci, cj, cg,)).fetchall()
                print("1")
            elif not cp and ca:
                buku = db.execute('SELECT isbn,judul,genre,sinopsis,status FROM buku WHERE isbn LIKE ? AND judul LIKE ? AND genre LIKE ? '
                ' AND status = ? AND flag = "on"',(ci, cj, cg, ca,)).fetchall()
                print("2")
            elif cp and not ca:
                buku = db.execute('SELECT isbn,judul,genre,sinopsis,status FROM buku WHERE isbn LIKE ? AND judul LIKE ? AND genre LIKE ? '
                ' AND status = ? AND flag = "on"',(ci, cj, cg, cp,)).fetchall()
                print("3")
            elif cp and ca:
                buku = db.execute('SELECT isbn,judul,genre,sinopsis,status FROM buku WHERE isbn LIKE ? AND judul LIKE ? AND genre LIKE ? '
                ' AND flag = "on"',(ci, cj, cg,)).fetchall()
                print("4")

    export_buku = ['ISBN', 'JUDUL', 'GENRE', 'SINOPSIS', 'STATUS BUKU']
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(export_buku)
    cw.writerows(buku)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=databuku.csv"
    output.headers["Content-type"] = "text/csv"
    print(ci,cj,cg,cp,ca)
    return output

@bp.route('/downloadformatbuku', methods=('GET','POST'))
@login_required
def downloadformatbuku():
    db = get_db()
    ci = ''
    buku = ''
    if request.method == 'POST':

        if 'downloadformatbuku' in request.form:

            cariisbn  = ci = request.form['ci']

            ci = p = "%"
            ci += str(cariisbn)
            ci += p

            buku = db.execute('SELECT isbn,judul,genre,sinopsis,status FROM buku WHERE isbn LIKE ?'
                ' AND flag = "on"',(ci,)).fetchall()

    export_buku = ['ISBN', 'JUDUL', 'GENRE', 'SINOPSIS']
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(export_buku)
    cw.writerows(buku)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=databuku.csv"
    output.headers["Content-type"] = "text/csv"
    return output
###########################################################################################################################
# DILANJUT SAMPE SINI# DILANJUT SAMPE SINI# DILANJUT SAMPE SINI# DILANJUT SAMPE SINI# DILANJUT SAMPE SINI# DILANJUT SAMPE SINI
############################################################################################################################
@bp.route('/uploadbuku', methods=('GET','POST'))
@login_required
def uploadbuku():
    db = get_db()
    isbn = isbnin = judul = genre = sinopsis = ''
    statusada = "ada"
    statusdipinjam = "dipinjam"
    flag = "update"

    if request.method == 'POST':

        if 'uploaddatabuku' in request.form:
            filebuku = request.files['filebuku']
            if filebuku.filename != '':
                #set_filename (waktu upload_nama file)
                timefilename = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y_%H.%M.%S..%f_')
                timefilename += filebuku.filename
                #cursor path ke static/files
                filepath = os.path.join(app.config['UPLOAD_FOLDER_BUKU'], timefilename)
                #save file on path static/files
                filebuku.save(filepath)
                with open(filepath) as file:
                    csv_filebukulen = csv.reader(file)
                    length = len(list(csv_filebukulen)[0])
                    print(10,length)
                    if length == 4:
                        with open(filepath) as file:
                            csv_filebukuhead = csv.reader(file)
                            isbn, judul, genre, sinopsis = list(csv_filebukuhead)[0]
                            print(0,isbn, judul, genre, sinopsis)
                            if isbn == 'ISBN' and judul == 'JUDUL' and genre == 'GENRE' and sinopsis == 'SINOPSIS':
                                with open(filepath) as file:
                                    csv_filebuku = csv.reader(file)
                                    next(csv_filebuku)
                                    for row in csv_filebuku:
                                        isbn = list(row)[0]
                                        judul = list(row)[1]
                                        genre = list(row)[2]
                                        sinopsis = list(row)[3]
                                        if isbn and judul and genre and sinopsis:
                                            datasama = db.execute('SELECT isbn FROM buku WHERE isbn = ?', (isbn,)).fetchone()
                                            if datasama:
                                                datadipinjam = db.execute('SELECT isbn FROM buku WHERE isbn = ? AND status = "dipinjam"', (isbn,)).fetchone()
                                                if datadipinjam:
                                                    isbnin = db.execute('SELECT isbn FROM buku WHERE isbn = ?', (isbn,)).fetchone()[0]
                                                    isbnold = isbnio = str(db.execute('SELECT isbn FROM buku WHERE isbn = ?', (isbnin,)).fetchone()[0])
                                                    judulold = str(db.execute('SELECT judul FROM buku WHERE isbn = ?', (isbnin,)).fetchone()[0])
                                                    genreold = str(db.execute('SELECT genre FROM buku WHERE isbn = ?', (isbnin,)).fetchone()[0])
                                                    sinopsisold = str(db.execute('SELECT sinopsis FROM buku WHERE isbn =?', (isbnin,)).fetchone()[0])
                                                    strold = "_updated_"
                                                    epoch = str(time.time())
                                                    isbnold += strold
                                                    isbnold += epoch
                                                    db.execute(
                                                        'UPDATE buku SET isbn = ?, judul = ?, genre = ?, sinopsis = ?, updated_at = CURRENT_TIMESTAMP, updated_by = ?, flag = ?'
                                                        ' WHERE isbn = ?', (isbnold, judulold, genreold, sinopsisold, g.admin['nama'], flag, isbnin,)
                                                    )
                                                    db.commit()
                                                    db.execute(
                                                        'INSERT INTO buku (isbn, judul, genre, sinopsis, status, created_by)'
                                                        ' VALUES (?, ?, ?, ?, ?, ?)', (isbnio, judulold, genreold, sinopsis, statusdipinjam, g.admin['nama'],)
                                                        )
                                                    db.commit()
                                                    print(1,isbn,judul,genre,sinopsis)
                                                elif not datadipinjam:
                                                    isbnin = db.execute('SELECT isbn FROM buku WHERE isbn = ?', (isbn,)).fetchone()[0]
                                                    isbnold = isbnio = str(db.execute('SELECT isbn FROM buku WHERE isbn = ?', (isbnin,)).fetchone()[0])
                                                    judulold = str(db.execute('SELECT judul FROM buku WHERE isbn = ?', (isbnin,)).fetchone()[0])
                                                    genreold = str(db.execute('SELECT genre FROM buku WHERE isbn = ?', (isbnin,)).fetchone()[0])
                                                    sinopsisold = str(db.execute('SELECT sinopsis FROM buku WHERE isbn =?', (isbnin,)).fetchone()[0])
                                                    strold = "_updated_"
                                                    epoch = str(time.time())
                                                    isbnold += strold
                                                    isbnold += epoch
                                                    db.execute(
                                                        'UPDATE buku SET isbn = ?, judul = ?, genre = ?, sinopsis = ?, updated_at = CURRENT_TIMESTAMP, updated_by = ?, flag = ?'
                                                        ' WHERE isbn = ?', (isbnold, judulold, genreold, sinopsisold, g.admin['nama'], flag, isbnin,)
                                                    )
                                                    db.commit()
                                                    db.execute(
                                                        'INSERT INTO buku (isbn, judul, genre, sinopsis, status, created_by)'
                                                        ' VALUES (?, ?, ?, ?, ?, ?)', (isbn, judul, genre, sinopsis, statusada, g.admin['nama'],)
                                                        )
                                                    db.commit()
                                                    print(2,isbn,judul,genre,sinopsis)
                                            elif not datasama:
                                                db.execute(
                                                        'INSERT INTO buku (isbn, judul, genre, sinopsis, status, created_by)'
                                                        ' VALUES (?, ?, ?, ?, ?, ?)', (isbn, judul, genre, sinopsis, statusada, g.admin['nama'],)
                                                        )
                                                db.commit()
                                                print(3,isbn,judul,genre,sinopsis)
                                        else:
                                            next(csv_filebuku)
                            else:
                                flash('GAGAL MENGUPLOAD COBA CEK KEMBALI PENAMAANNYA')
                    else:
                        flash('GAGAL MENGUPLOAD COBA CEK KEMBALI FORMATNYA')
    db.close()
    return redirect(url_for('perpus.tambahbuku'))

def get_buku(id): #### Mendapat Data buku berdasarkan id ####
    getbuku = get_db().execute(
        'SELECT * FROM buku WHERE id = ?', (id,)).fetchone()

    if getbuku is None:
        abort(404, f"buku dengan id {id} tidak ditemukan")

    return getbuku

@bp.route('/updatebukuada/<int:id>', methods=('GET', 'POST'))
@login_required
def updatebukuada(id): #### Fungsi Update Buku ####
    getbuku = get_buku(id)
    db = get_db()
    isbnold = str(db.execute('SELECT isbn FROM buku WHERE id = ?', (id,)).fetchone()[0])
    judulold = str(db.execute('SELECT judul FROM buku WHERE id = ?', (id,)).fetchone()[0])
    genreold = str(db.execute('SELECT genre FROM buku WHERE id = ?', (id,)).fetchone()[0])
    sinopsisold = str(db.execute('SELECT sinopsis FROM buku WHERE id =?', (id,)).fetchone()[0])
    strold = "_updated_"
    epoch = str(time.time())
    isbnold += strold
    isbnold += epoch
    if request.method == 'POST':
        isbn = request.form['isbn']
        judul = request.form['judul']
        genre = request.form['genre']
        sinopsis = request.form['sinopsis']
        status = request.form['status']
        flag = request.form['flag']
        error = None

        if not isbn:
            error = 'masukkan kode isbn'
        elif not judul:
            error = 'masukkan judul'
        elif not genre:
            error = 'masukkan genre'
        elif not sinopsis:
            error = 'tulis sinopsisnya'
            
        if error is None:
            db.execute(
                'UPDATE buku SET isbn = ?, judul = ?, genre = ?, sinopsis = ?, updated_at = CURRENT_TIMESTAMP, updated_by = ?, flag = ?'
                ' WHERE id = ?', (isbnold, judulold, genreold, sinopsisold, g.admin['nama'], flag, id,)
            )
            db.commit()
            db.execute(
                'INSERT INTO buku (isbn, judul, genre, sinopsis, status, created_by)'
                ' VALUES (?, ?, ?, ?, ?, ?)', (isbn, judul, genre, sinopsis, status, g.admin['nama'],)
                )
            db.commit()
            db.close()
            return redirect(url_for('perpus.tambahbuku'))

        else:
            flash(error)
        
    return render_template('perpus/updatebukuada.html', getbuku=getbuku)

@bp.route('/updatebukudipinjam/<int:id>', methods=('GET', 'POST'))
@login_required
def updatebukudipinjam(id): #### Fungsi Update Buku ####
    getbuku = get_buku(id)
    db = get_db()
    isbnold = str(db.execute('SELECT isbn FROM buku WHERE id = ?', (id,)).fetchone()[0])
    judulold = str(db.execute('SELECT judul FROM buku WHERE id = ?', (id,)).fetchone()[0])
    genreold = str(db.execute('SELECT genre FROM buku WHERE id = ?', (id,)).fetchone()[0])
    sinopsisold = str(db.execute('SELECT sinopsis FROM buku WHERE id =?', (id,)).fetchone()[0])
    strold = "_updated_"
    epoch = str(time.time())
    isbnold += strold
    isbnold += epoch
    if request.method == 'POST':
        isbn = request.form['isbn']
        judul = request.form['judul']
        genre = request.form['genre']
        sinopsis = request.form['sinopsis']
        status = request.form['status']
        flag = request.form['flag']
        error = None

        if not isbn:
            error = 'masukkan kode isbn'
        elif not judul:
            error = 'masukkan judul'
        elif not genre:
            error = 'masukkan genre'
        elif not sinopsis:
            error = 'tulis sinopsisnya'
            
        if error is None:
            db.execute(
                'UPDATE buku SET isbn = ?, judul = ?, genre = ?, sinopsis = ?, updated_at = CURRENT_TIMESTAMP, updated_by = ?, flag = ?'
                ' WHERE id = ?', (isbnold, judulold, genreold, sinopsisold, g.admin['nama'], flag, id,)
            )
            db.commit()
            db.execute(
                'INSERT INTO buku (isbn, judul, genre, sinopsis, status, created_by)'
                ' VALUES (?, ?, ?, ?, ?, ?)', (isbn, judul, genre, sinopsis, status, g.admin['nama'],)
                )
            db.commit()
            db.close()
            return redirect(url_for('perpus.tambahbuku'))

        else:
            flash(error)
        
    return render_template('perpus/updatebukudipinjam.html', getbuku=getbuku)

@bp.route('/deletebuku/<int:id>', methods=('POST',))
@login_required
def deletebuku(id): #### Fungsi Delete Buku ####
    get_buku(id)
    epoch = str(time.time())
    delstr = "_deleted_"
    db = get_db()
    isbn = str(db.execute('SELECT isbn FROM buku WHERE id = ?', (id,)).fetchone()[0])
    isbn += delstr
    isbn += epoch
    db.execute(
    'UPDATE buku SET isbn = ?, flag = "deleted", updated_at = CURRENT_TIMESTAMP, updated_by=? WHERE id = ?', (isbn, g.admin['nama'], id,)
    )
    db.commit()
    db.close()
    return redirect(url_for('perpus.tambahbuku'))


##############################################################################

##################################### member ################################
@bp.route('/tambahmember', methods=('GET', 'POST'))
@login_required
def tambahmember():
    db = get_db()
    member = searchmember()[0]
    ci = searchmember()[1]
    cni = searchmember()[2]
    cna = searchmember()[3]
    cj = searchmember()[4]
    ca = searchmember()[5]
    if request.method == 'POST':
        if 'tambahmember' in request.form:
            idmember = request.form['idmember']
            nik = request.form['nik']
            nama = request.form['nama']
            jenis_kelamin = request.form['jenis_kelamin']
            alamat = request.form['alamat']
            datamember = db.execute('SELECT idmember FROM member WHERE idmember = ? ', (idmember,)).fetchone()
            error = None

            if not idmember:
                error = 'masukkan id member'
            elif not nik:
                error = 'masukkan nik'
            elif not nama:
                error = 'masukkan nama'
            elif not jenis_kelamin:
                error = 'masukkan jenis kelamin'
            elif not alamat:
                error = 'masukkan alamat'
            elif datamember is not None:
                error = 'id member sudah terpakai'
            
            if error is None:
                db.execute(
                    'INSERT INTO member (idmember, nik, nama, jenis_kelamin, alamat, created_by)'
                    ' VALUES (?, ?, ?, ?, ?, ?)', (idmember, nik, nama, jenis_kelamin, alamat, g.admin['nama'])
                )
                db.commit()
                db.close()
                return redirect(url_for('perpus.tambahmember'))

            flash(error)

    return render_template('perpus/tambahmember.html', member=member, ci=ci, cni=cni, cna=cna, cj=cj, ca=ca)

def searchmember():
    db = get_db()
    ci = cni = cna = cj = ca = ''
    member = db.execute('SELECT * FROM member WHERE flag = "on"').fetchall()
    if request.method == 'POST':

        if 'caridatamember' in request.form:
            cariidmember  = ci = request.form['cariidmember']
            carinik = cni = request.form['carinik']
            carinama = cna = request.form['carinama']
            carijenis = cj = request.form.get('carijenis')
            carialamat = ca = request.form.get('carialamat')
            ci = cni = cna = cj = ca = p = "%"
            ci += str(cariidmember)
            ci += p
            cni += str(carinik)
            cni += p
            cna += str(carinama)
            cna += p
            cj += str(carijenis)
            cj += p
            ca += str(carialamat)
            ca += p
            member = db.execute('SELECT * FROM member '
            ' WHERE idmember LIKE ? AND nik LIKE ? AND nama LIKE ? AND jenis_kelamin LIKE ? AND alamat LIKE ?'
            ' AND flag = "on"',(ci,cni,cna,cj,ca,)).fetchall()
    return member, ci, cni, cna, cj, ca            

@bp.route('/downloadmember', methods=('GET','POST'))
@login_required
def downloadmember():
    db = get_db()
    ci = cni = cna = cj = ca = ''
    member = db.execute('SELECT idmember,nik,nama,jenis_kelamin,alamat FROM member WHERE flag = "on"').fetchall()

    if request.method == 'POST':

        if 'downloaddatamember' in request.form:
            cariidmember  = ci = request.form['ci']
            carinik = cni = request.form['cni']
            carinama = cna = request.form['cna']
            carijenis = cj = request.form.get('cj')
            carialamat = ca = request.form.get('ca')
            ci = cni = cna = cj = ca = p = "%"
            ci += str(cariidmember)
            ci += p
            cni += str(carinik)
            cni += p
            cna += str(carinama)
            cna += p
            cj += str(carijenis)
            cj += p
            ca += str(carialamat)
            ca += p
            member = db.execute('SELECT idmember,nik,nama,jenis_kelamin,alamat FROM member '
            ' WHERE idmember LIKE ? AND nik LIKE ? AND nama LIKE ? AND jenis_kelamin LIKE ? AND alamat LIKE ?'
            ' AND flag = "on"',(ci,cni,cna,cj,ca,)).fetchall()

    export_member = ['ID MEMBER', 'NO TANDA PENGENAL', 'NAMA MEMBER', 'JENIS KELAMIN', 'ALAMAT']
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(export_member)
    cw.writerows(member)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=datamember.csv"
    output.headers["Content-type"] = "text/csv"
    print(ci,cni,cna,cj,ca)
    return output

@bp.route('/downloadformatmember', methods=('GET','POST'))
@login_required
def downloadformatmember():
    db = get_db()
    ci = ''
    member = ''
    if request.method == 'POST':

        if 'downloadformatmember' in request.form:
            cariidmember  = ci = request.form['ci']
            ci = p = "%"
            ci += str(cariidmember)
            ci += p
            member = db.execute('SELECT idmember,nik,nama,jenis_kelamin,alamat FROM member '
            ' WHERE idmember LIKE ?'
            ' AND flag = "on"',(ci,)).fetchall()

    export_member = ['ID MEMBER', 'NO TANDA PENGENAL', 'NAMA MEMBER', 'JENIS KELAMIN', 'ALAMAT']
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(export_member)
    cw.writerows(member)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=datamember.csv"
    output.headers["Content-type"] = "text/csv"

    return output

@bp.route('/uploadmember', methods=('GET', 'POST'))
@login_required
def uploadmember():
    db = get_db()
    idmember = idmemberin = nik = nama = jenis_kelamin = alamat = ''
    flag = "updated"

    if request.method == 'POST':

        if 'uploaddatamember' in request.form:
            filemember = request.files['filemember']
            if filemember.filename != '':
                #set filename (Waktu upload_nama file)
                timefilename = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y_%H.%M.%S..%f_')
                timefilename += filemember.filename
                #set path
                filepath = os.path.join(app.config['UPLOAD_FOLDER_MEMBER'], timefilename)
                #save file on path static/files
                filemember.save(filepath)
                with open(filepath) as file:
                    csv_filememberlen = csv.reader(file)
                    length = len(list(csv_filememberlen)[0])
                    print(0, length)
                    if length == 5:
                        with open(filepath) as file:
                            csv_filememberhead = csv.reader(file)
                            idmember, nik, nama, jenis_kelamin, alamat = list(csv_filememberhead)[0]
                            if idmember == 'ID MEMBER' and nik == 'NO TANDA PENGENAL' and nama == 'NAMA MEMBER' and jenis_kelamin == 'JENIS KELAMIN' and alamat == 'ALAMAT':
                                with open(filepath) as file:
                                    csv_filemember = csv.reader(file)
                                    next(csv_filemember)
                                    for row in csv_filemember:
                                        idmember = list(row)[0]
                                        nik = list(row)[1]
                                        nama = list(row)[2]
                                        jenis_kelamin = list(row)[3]
                                        alamat = list(row)[4]
                                        if idmember and nik and nama and jenis_kelamin and alamat:
                                            datasama = db.execute('SELECT idmember FROM member WHERE idmember = ?', (idmember,)).fetchone()
                                            if datasama:
                                                idmemberin = db.execute('SELECT idmember FROM member WHERE idmember = ?', (idmember,)).fetchone()[0]
                                                idmemberold = str(db.execute('SELECT idmember FROM member WHERE idmember = ?', (idmemberin,)).fetchone()[0])
                                                nikold = str(db.execute('SELECT nik FROM member WHERE idmember = ?', (idmemberin,)).fetchone()[0])
                                                namaold = str(db.execute('SELECT nama FROM member WHERE idmember = ?', (idmemberin,)).fetchone()[0])
                                                jenis_kelaminold = str(db.execute('SELECT jenis_kelamin FROM member WHERE idmember = ?', (idmemberin,)).fetchone()[0])
                                                alamatold = str(db.execute('SELECT alamat FROM member WHERE idmember = ?', (idmemberin,)).fetchone()[0])
                                                strold = "_updated_"
                                                epoch = str(time.time())
                                                idmemberold += strold
                                                idmemberold += epoch
                                                db.execute(
                                                    'UPDATE member SET idmember = ?, nik = ?, nama = ?, jenis_kelamin = ?, alamat = ?, updated_at = CURRENT_TIMESTAMP, updated_by = ?, flag = ?'
                                                    ' WHERE idmember = ?', (idmemberold, nikold, namaold, jenis_kelaminold, alamatold, g.admin['nama'], flag, idmemberin,)
                                                )
                                                db.commit()
                                                db.execute(
                                                    'INSERT INTO member (idmember, nik, nama, jenis_kelamin, alamat, created_by)'
                                                    ' VALUES (?, ?, ?, ?, ?, ?)', (idmember, nik, nama, jenis_kelamin, alamat, g.admin['nama'],)
                                                    )
                                                db.commit()
                                                print(1,idmember,nik,nama,jenis_kelamin,alamat)
                                                print(2,idmemberold,nikold,namaold,jenis_kelaminold,alamatold)
                                            elif not datasama:
                                                db.execute(
                                                    'INSERT INTO member (idmember, nik, nama, jenis_kelamin, alamat, created_by)'
                                                    ' VALUES (?, ?, ?, ?, ?, ?)', (idmember, nik, nama, jenis_kelamin, alamat, g.admin['nama'],)
                                                    )
                                                db.commit()
                                                print(3,idmember,nik,nama,jenis_kelamin,alamat)
                                        else:
                                            next(csv_filebuku)
                            else:
                                flash('GAGAL MENGUPLOAD COBA CEK KEMBALI PENAMAANNYA')
                    else:
                        flash('GAGAL MENGUPLOAD COBA CEK KEMBALI FORMATNYA')
    db.close()    
    return redirect(url_for('perpus.tambahmember'))
            
def get_member(id): #### Mendapat Data member berdasarkan id ####
    getmember = get_db().execute(
        'SELECT * FROM member WHERE id = ?', (id,)).fetchone()

    if getmember is None:
        abort(404, f"member dengan id {id} tidak ditemukan")

    return getmember

@bp.route('/updatemember/<int:id>', methods=('GET', 'POST'))
@login_required
def updatemember(id): #### Fungsi Update Member ####
    getmember = get_member(id)
    db = get_db()
    idmemberold = str(db.execute('SELECT idmember FROM member WHERE id = ?', (id,)).fetchone()[0])
    nikold = str(db.execute('SELECT nik FROM member WHERE id = ?', (id,)).fetchone()[0])
    namaold = str(db.execute('SELECT nama FROM member WHERE id = ?', (id,)).fetchone()[0])
    jenis_kelaminold = str(db.execute('SELECT jenis_kelamin FROM member WHERE id = ?', (id,)).fetchone()[0])
    alamatold = str(db.execute('SELECT alamat FROM member WHERE id = ?', (id,)).fetchone()[0])
    strold = "_updated_"
    epoch = str(time.time())
    idmemberold += strold
    idmemberold += epoch
    if request.method == 'POST':
        idmember = request.form['idmember']
        nik = request.form['nik']
        nama = request.form['nama']
        jenis_kelamin = request.form['jenis_kelamin']
        alamat = request.form['alamat']
        flag = request.form['flag']
        error = None

        if not idmember:
            error = 'masukkan id member'
        elif not nik:
            error = 'masukkan nik'
        elif not nama:
            error = 'masukkan nama'
        elif not jenis_kelamin:
            error = 'masukkan jenis kelamin'
        elif not alamat:
            error = 'masukkan alamat'
            
        if error is None:
            db.execute(
                'UPDATE member SET idmember = ?, nik = ?, nama = ?, jenis_kelamin = ?, alamat = ?, updated_at = CURRENT_TIMESTAMP, updated_by = ?, flag = ?'
                ' WHERE id = ?', (idmemberold, nikold, namaold, jenis_kelaminold, alamatold, g.admin['nama'], flag, id,)
            )
            db.commit()
            db.execute(
                'INSERT INTO member (idmember, nik, nama, jenis_kelamin, alamat, created_by)'
                ' VALUES (?, ?, ?, ?, ?, ?)', (idmember, nik, nama, jenis_kelamin, alamat, g.admin['nama'],)
                )
            db.commit()
            db.close()
            return redirect(url_for('perpus.tambahmember'))

        else:
            flash(error)
        
    return render_template('perpus/updatemember.html', getmember=getmember)

@bp.route('/deletemember/<int:id>', methods=('POST',))
@login_required
def deletemember(id): #### Fungsi Delete Buku ####
    get_member(id)
    epoch = str(time.time())
    delstr = "_deleted_"
    db = get_db()
    idmember = str(db.execute('SELECT idmember FROM member WHERE id = ?', (id,)).fetchone()[0])
    idmember += delstr
    idmember += epoch
    db.execute(
    'UPDATE member SET idmember = ?, flag = "inaktif", updated_at = CURRENT_TIMESTAMP, updated_by=? WHERE id = ?', (idmember, g.admin['nama'], id,)
    )
    db.commit()
    db.close()
    return redirect(url_for('perpus.tambahmember'))
#############################################################################

#################################### transaksi ##############################
@bp.route('/tambahtransaksi', methods=('GET', 'POST'))
@login_required
def tambahtransaksi():
    db = get_db()
    if request.method == 'POST':
        idmember = request.form['idmember']
        isbn = request.form['isbn']
        tgl_kembali = request.form['tgl_kembali']
        flag = request.form['flag']
        datamember = db.execute('SELECT idmember FROM member WHERE idmember = ? ', (idmember,)).fetchone()
        databuku = db.execute('SELECT isbn FROM buku WHERE isbn = ? ', (isbn,)).fetchone()
        datapinjam = db.execute('SELECT isbn FROM buku WHERE isbn = ? AND status = "ada"', (isbn,)).fetchone()
        error = None

        if not idmember:
            error = 'masukkan id member'
        elif not isbn:
            error = 'masukkan kode isbn'
        elif not tgl_kembali:
            error = 'masukkan tanggal pengembalian'
        elif not databuku and not datamember:
            error = 'Data member dan buku tidak ditemukan'
        elif not datamember:
            error = 'Data member tidak ditemukan'
        elif databuku and not datapinjam:
            error = 'Buku sedang dipinjam'
        elif not databuku:
            error = 'Data buku tidak ditemukan'
        
        if error is None:
            db.execute(
                'INSERT INTO transaksi(idmember, isbn, tgl_kembali, idadmin, created_by, flag)'
                ' VALUES (?, ?, ?, ?, ?, ?)', (idmember, isbn, tgl_kembali, g.admin['id'], g.admin['nama'], flag,)
            )
            db.commit()
            db.execute(
                'UPDATE buku SET status = "dipinjam" WHERE isbn = ?', (isbn,)
            )
            db.commit()
            db.close()
            return redirect(url_for('index'))
            

        flash(error)

    return render_template('perpus/tambahtransaksi.html')

def get_transaksi(id):
    gettransaksi = get_db().execute(
        'SELECT * FROM transaksi WHERE id = ?', (id,)).fetchone()

    if gettransaksi is None:
        abort(404, f"transaksi dengan id {id} tidak ditemukan")

    return gettransaksi

@bp.route('/updatetransaksi/<int:id>', methods=('GET', 'POST'))
@login_required
def updatetransaksi(id):
    gettransaksi = get_transaksi(id)
    db = get_db()
    if request.method == 'POST':
        idmember = request.form['idmember']
        isbn = request.form['isbn']
        tgl_kembali = request.form['tgl_kembali']
        flag = request.form['flag']
        error = None

        if not isbn:
            error = 'masukkan kode isbn'
        elif not idmember:
            error = 'masukkan id member'
        elif not tgl_kembali:
            error = 'masukkan tanggal kembali'

        if error is None:
            db.execute(
                'UPDATE buku SET status = "ada" WHERE isbn = ?', (isbn,)
            )
            db.commit()
            db.execute(
                'UPDATE transaksi SET  updated_at = CURRENT_TIMESTAMP, updated_by=?, flag = ? WHERE id = ?', (g.admin['nama'], flag, id,)
            )
            db.commit()
            return redirect(url_for('index'))

        else:
            flash(error)
        
    return render_template('perpus/updatetransaksi.html', gettransaksi=gettransaksi)

#############################################################################

##############################################################################
# note: MENAMBAH DAN MEMPERBAIKI FITUR SEARCH MEMBER DAN TRANSAKSI 
# MENGINTEGRASIKAN EXPORT CSV DENGAN QUERY FITUR SEARCH