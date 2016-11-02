 drop database if exists trampolim;

 create database trampolim
     DEFAULT CHARACTER SET utf8;             -- creates working database

 show databases;                             -- show server databases
 use trampolim;                              -- set system database 'trampolim' as the current database
 select database();                          -- shows current database
 set foreign_key_checks=0;

 create table admin(
     username varchar(255) not null,
     password varchar(255) not null,
     PRIMARY KEY (username)
 );

 create table validadores(
     num_serie varchar(255) not null,
     id_onibus int,
     PRIMARY KEY (num_serie),
     FOREIGN KEY (id_onibus) REFERENCES onibus(id_onibus)
 );

 create table onibus(
     id_onibus int not null ,
     id_validador varchar(255) not null,
     PRIMARY KEY (id_onibus),
     FOREIGN KEY (id_validador) REFERENCES validadores(num_serie)
 );

 create table gre(
     id_gre int not null auto_increment,
     data_envio date not null,
     id_onibus int not null,
     remessa int not null,
     id_validador varchar(255) not null,
     PRIMARY KEY (id_gre),
     FOREIGN KEY (id_onibus) REFERENCES onibus(id_onibus),
     FOREIGN KEY (id_validador) REFERENCES validadores(num_serie)
 );

 create table defeito(
     tipo_defeito varchar(255) not null,
     PRIMARY KEY (tipo_defeito)
 );

 create table lista_defeitos(
     id_gre int not null,
     tipo_defeito varchar(255) not null,
     relatorio varchar(255),
     CONSTRAINT pk_listaID PRIMARY KEY (id_gre,tipo_defeito),
     FOREIGN KEY (id_gre) REFERENCES gre(id_gre),
     FOREIGN KEY (tipo_defeito) REFERENCES defeito(tipo_defeito)
 );

show tables;
describe admin;
describe validadores;
describe onibus;
describe gre;
describe defeito;
describe lista_defeitos;
