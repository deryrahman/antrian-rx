# Antrian Resep
RSUD Cilacap bagian farmasi

## Instalasi:
1. Pastikan python yang dijalankan adalah python3
```
$ python -V
```
2. Pastikan pip terinstall, jika belum, run command:
```
$ sudo apt-get install python-pip python-dev build-essential
```
3. Import semua package yang diperlukan, run command:
```
$ pip install -r requirements.txt
```
4. Set environment variable untuk :
    - MONGO_DBNAME : (string) nama database mongodb, eg: 'test'
    - MONGO_URI : (string) uri mongodb, eg 'mongodb://{user}:{password}@localhost:27017/test'
    - SECRET_KEY : (string) secret key yang digunakan untuk applikasi, eg 'coba-coba'
5. Untuk menjalankan aplikasi, jalankan gunicorn, run command:
```
$ gunicorn server:app :8000 -n antrian-rx
```
Aplikasi akan berjalan di port 8000, eg. `http://localhost:8000`
6. Untuk mematikan, ctrl+C
7. Untuk menjalankan aplikasi pada background proses, jalankan `start.sh`, run command:
```
$ ./start.sh
```
8. Untuk mematikan aplikasi pada background proses, jalankan `stop.sh`, run command:
```
$ ./stop.sh
```
Pastikan, chmod untuk file start.sh dan stop.sh sudah benar. Jika belum, run command:
```
$ sudo chmod +x start.sh && sudo chmod +x stop.sh
```
