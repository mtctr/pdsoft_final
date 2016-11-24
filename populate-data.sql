insert into admin values ("admin", "admin");

insert into validadores(num_serie)
values("a1b2c3");
insert into validadores(num_serie)
values("a1b2c4");
insert into validadores(num_serie)
values("a1b2c5");
insert into validadores(num_serie)
values("b1b2c5");
insert into validadores(num_serie)
values("a1b3c3");
insert into validadores(num_serie)
values("a1bs2");
insert into validadores(num_serie)
values("ds1s23");
insert into validadores(num_serie)
values("ds22c21");
insert into validadores(num_serie)
values("f43e32");
insert into validadores(num_serie)
values("e323s2");
insert into validadores(num_serie)
values("2332d3");
insert into validadores(num_serie)
values("d32432");


insert into onibus(id_onibus, id_validador)
values(1000, "a1b2c3");
insert into onibus(id_onibus, id_validador)
values(2000, "a1b2c4");
insert into onibus(id_onibus, id_validador)
values(1001, "a1b2c5");
insert into onibus(id_onibus, id_validador)
values(1002, "f43e32");
insert into onibus(id_onibus, id_validador)
values(2001, "2332d3");
insert into onibus(id_onibus, id_validador)
values(1003, "d32432");
insert into onibus(id_onibus, id_validador)
values(1032, "ds22c21");
insert into onibus(id_onibus, id_validador)
values(2002, "a1b2c4");
insert into onibus(id_onibus, id_validador)
values(1021, "a1b2c5");

insert into defeito values("Placa defeituosa");
insert into defeito values("Visor falho");
insert into defeito values("Leitor de cartão");
insert into defeito values("Conexão com sistema");
insert into defeito values("LEDs falhos");

insert into gre(data_envio, data_retorno, id_onibus, remessa, id_validador)
values("2016-11-23", "2016-11-24",1000,20323,"a1b2c3");
insert into lista_defeitos(id_gre, tipo_defeito)
values(1,"Placa defeituosa");

insert into gre(data_envio, data_retorno, id_onibus, remessa, id_validador)
values("2016-11-24", "2016-11-24",1001,20323,"a1b2c4");
insert into lista_defeitos(id_gre, tipo_defeito)
values(2,"Leitor de cartão");

insert into gre(data_envio, data_retorno, id_onibus, remessa, id_validador)
values("2016-11-20", "2016-11-24",1001,20323,"a1b2c5");
insert into lista_defeitos(id_gre, tipo_defeito)
values(3,"Leitor de cartão");

insert into gre(data_envio, data_retorno, id_onibus, remessa, id_validador)
values("2016-11-21", "2016-11-24",1001,20323,"a1b2c4");
insert into lista_defeitos(id_gre, tipo_defeito)
values(4,"Leitor de cartão");

insert into gre(data_envio, data_retorno, id_onibus, remessa, id_validador)
values("2016-11-22", "2016-11-24",1002,20323,"a1b2c5");
insert into lista_defeitos(id_gre, tipo_defeito)
values(5,"Leitor de cartão");

insert into gre(data_envio, data_retorno, id_onibus, remessa, id_validador)
values("2016-11-22", "2016-11-24",1002,20323,"a1b2c5");
insert into lista_defeitos(id_gre, tipo_defeito)
values(6,"LEDs falhos");

insert into gre(data_envio, data_retorno, id_onibus, remessa, id_validador)
values("2016-11-24", "2016-11-24",1000,20323,"a1b2c5");
insert into lista_defeitos(id_gre, tipo_defeito)
values(7,"LEDs falhos");

insert into gre(data_envio, data_retorno, id_onibus, remessa, id_validador)
values("2016-11-19", "2016-11-24",1003,20323,"a1b2c3");
insert into lista_defeitos(id_gre, tipo_defeito)
values(8,"Conexão com sistema");

insert into gre(data_envio, data_retorno, id_onibus, remessa, id_validador)
values("2016-11-23", "2016-11-24",1021,20323,"a1b2c3");
insert into lista_defeitos(id_gre, tipo_defeito)
values(9,"Placa defeituosa");
