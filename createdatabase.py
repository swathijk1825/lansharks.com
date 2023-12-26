#!/usr/bin/env python3
import mysql.connector

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'P@ssw0rd'
)

cursor = db.cursor()

cursor.execute('CREATE DATABASE python')

cursor.execute('USE python')
cursor.execute('CREATE TABLE users (userID INT, userName varchar(25), password varchar(25), type varchar(1))')

sql = 'INSERT INTO users (userID, userName, password, type) VALUES (%s, %s, %s, %s)'
value = [
    (1, 'msato', 'P@ssw0rd', 'e'),
    (2, 'hbyrne', 'P@ssw0rd', 'e'),
    (3, 'dlaghari', 'P@ssw0rd', 'c'),
    (4, 'pzielinski', 'P@ssw0rd', 'c'),
    (5, 'imorales', 'P@ssw0rd', 'c')
]

cursor.executemany(sql, value)
db.commit()

cursor.execute('CREATE TABLE incidents (incidentID INT AUTO_INCREMENT PRIMARY KEY, packetDateTime datetime, srcIP varchar(20), destIP varchar(20), protocol varchar(10), srcPort varchar(10), destPort varchar(10), hostIP varchar(20), serverIP varchar(20), srcMac varchar(20), destMac varchar(20), info text, customerNumber int)')

sql = 'INSERT INTO incidents (packetDateTime, srcIP, destIP, protocol, srcPort, destPort, hostIP, serverIP, srcMac, destMac, info, customerNumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
value = [
    ('2023-02-08 03:20:00','172.16.137.40','172.16.137.40', 'DHCP','68','67','172.16.137.40','172.16.137.1','08:00:2b:ef:ab:7c', '00:1d:7e:7c:c4:8d','DHCP Request  - Transaction ID 0xfe9ceb09', 1),
	('2023-03-08 13:20:15','172.16.137.1','172.16.137.1', 'DHCP','67','68','172.16.137.1','255.255.255.255','00:1d:7e:7c:c4:8d', 'ff:ff:ff:ff:ff:ff','DHCP ACK      - Transaction ID 0xfe9ceb09', 1),
	('2022-08-24 10:35:30','10.100.25.14','10.100.25.14', 'TCP','1065','139','10.100.25.14','10.100.18.12','00:15:c5:3c:4f:9e', '00:03:ff:6c:8b:24','1065  >  139 [SYN] Seq=0 Win=8 Len=0', 2),
	('2022-09-24 10:35:15','10.100.25.14','10.100.25.14', 'TCP','19491','135','10.100.25.14','10.100.18.12','00:15:c5:3c:4f:9e', '00:03:ff:6c:8b:24','19491  >  135 [SYN] Seq=0 Win=8 Len=0', 2),
	('2022-10-24 10:35:35','10.100.25.14','10.100.25.14', 'TCP','7358','445','10.100.25.14','10.100.18.12','00:15:c5:3c:4f:9e', '00:03:ff:6c:8b:24','7358  >  445 [SYN] Seq=0 Win=8 Len=0', 2),
	('2022-07-10 11:32:42','23.67.253.43','23.67.253.43', 'TCP','80','49163','54.10.120.45','192.168.137.83','a8:b1:d4:ac:fe:7d', '00:21:9b:5b:d1:7a','80  >  49163 [SYN, ACK] Seq=0 Ack=1 Win=14600 Len=0 MSS=1367 SACK_PERM=1 WS=32', 3), 
	('2022-08-10 11:32:55','192.168.137.83','192.168.137.83', 'TCP','49163','80','192.168.137.83','54.10.120.45','00:21:9b:5b:d1:7a', 'a8:b1:d4:ac:fe:7d','49163  >  80 [ACK] Seq=1 Ack=1 Win=65536 Len=0', 3),
	('2022-09-10 11:32:21','192.168.137.83','192.168.137.83', 'HTTP','49163','80','192.168.137.83','54.10.120.45','00:21:9b:5b:d1:7a', 'a8:b1:d4:ac:fe:7d','HEAD /v9/windowsupdate/redir/muv4wuredir.cab?1507101531 HTTP/1.1', 3),
	('2022-10-10 11:32:38','23.67.253.43','23.67.253.43', 'TCP','80','49163','54.10.120.45,192','168.137.83','a8:b1:d4:ac:fe:7d', '00:21:9b:5b:d1:7a','80  >  49163 [ACK] Seq=1 Ack=174 Win=15680 Len=0', 3)
]

cursor.executemany(sql, value)
db.commit()

cursor.execute('CREATE TABLE employees (empNumber INT AUTO_INCREMENT PRIMARY KEY, firstName varchar(25), lastName varchar(25), email varchar(50), position varchar(50))')

sql = 'INSERT INTO employees (firstName, lastName, email, position) VALUES (%s, %s, %s, %s)'
value = [
    ('Mia', 'Sato', 'msato@lansharks.com', 'President'),
    ('Hector', 'Byrne', 'hbyrne@lansharks.com', 'Vice President')
]

cursor.executemany(sql, value)
db.commit()

cursor.execute('CREATE TABLE customers (customerNumber INT AUTO_INCREMENT PRIMARY KEY, firstName varchar(25), lastName varchar(25), companyName varchar(50), address varchar(150), city varchar(50), state varchar(30), zipCode varchar(20), email varchar(50), phone varchar(15), comments text)')

sql = 'INSERT INTO customers (firstName, lastName, companyName, address, city, state, zipCode, email, phone, comments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
value = [
    ('Dhruv', 'Laghari', 'Mumbai Tea Room','E-13 Nand Dham Est, Marol Maroshi Road', 'Mumbai', 'Maharashtra', '400059', 'dlaghari@mumbaitearoom.com', '02266935079', 'Please email info.'),
	('Piotr', 'Zielinski', 'Warszawa Pub', 'ul.Wybrzeze Gdanskie 69', 'Warszawa', '', '00-280', 'piotr@warszawapub.com', '884063878', 'love the web site!'),
	('Isabel', 'Morales', 'Casa Flores', '600 Este de la Rotonda y Griega', 'Tierra Blanca', 'Cartago', '', 'isabel@casaflores.com', '22758081', 'Security is important. Call soon.')
]

cursor.executemany(sql, value)
db.commit()

cursor.execute('CREATE TABLE attacks (userID INT , attack_type varchar(25), info varchar(25), attacks varchar(50), time datetime)')


cursor.close()
db.close()