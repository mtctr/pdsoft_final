/*
 * my first mysql script - testscript.sql.
 * you need to run this script with an authorized user.
 */
 drop database if exists trampolim;

 create database trampolim
     DEFAULT CHARACTER SET utf8;             -- creates working database

 show databases;                             -- show server databases
 use trampolim;                              -- set system database 'trampolim' as the current database
 select database();                          -- shows current database

 create table admin(
     username varchar(255) not null,
     password varchar(255) not null,
     PRIMARY KEY (username)
 );

 create table Validadores(
     num_serie varchar(255) not null,
     id_onibus int,
     PRIMARY KEY (num_serie),
     FOREIGN KEY (id_onibus) REFERENCES Onibus(id_onibus)
 );

 create table Onibus(
     id_onibus int not null ,
     id_validador varchar(255) not null,
     PRIMARY KEY (id_onibus),
     FOREIGN KEY (id_validador) REFERENCES Validador(num_serie)
 );

 create table GRE(
     id_gre int not null auto_increment,
     data_envio date,
     id_onibus int,
     remessa int,
     id_validador varchar(255),
     PRIMARY KEY (id_gre),
     FOREIGN KEY (id_onibus) REFERENCES Onibus(id_onibus),
     FOREIGN KEY (id_validador) REFERENCES Validador(num_serie)
 );

 create table Defeito(
     tipo_defeito varchar(255) not null,
     PRIMARY KEY (tipo_defeito)
 );

 create table Lista_defeitos(
     id_gre int not null,
     tipo_defeito varchar(255) not null,
     relatorio varchar(255),
     CONSTRAINT pk_listaID PRIMARY KEY (id_gre,tipo_defeito),
     FOREIGN KEY (id_gre) REFERENCES GRE(id_gre),
     FOREIGN KEY (tipo_defeito) REFERENCES Defeito(tipo_defeito)
 );
