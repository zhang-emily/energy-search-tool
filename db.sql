

CREATE TABLE renewable_energy_consumption
    (state varchar(30),
    biomass float(10),
    hydropower float(10),
    solar float(10),
    wind float(10));

.separator ','
.import data/consumption_ranked_by_state_2017_renewable_energy_by_source.csv renewable_energy_consumption


CREATE TABLE energy_consumption_by_source
    (state varchar(30),
    coal float(10),
    natural_gas float(10),
    petroleum float(10),
    nuclear float(10),
    renewable float(10));

.separator ','
.import data/2017_energy_consumption_by_source.csv energy_consumption_by_source


CREATE TABLE price_expenditure
    (state varchar(30),
    prices float(10),
    expenditures float(10),
    exp_per_person float(10),
    exp_as_perc_of_gdp float(10));

.separator ','
.import data/prices_and_expenditures_ranked_by_state_2017_total_energy.csv price_expenditure


.mode column
.header ON