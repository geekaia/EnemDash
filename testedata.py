from flask import Flask

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go


######### Imported from bokeh #########
# import sqlite3
import pandas as pd


from sqlalchemy import create_engine
db = create_engine('postgresql://postgres:123@localhost/postgres')


########### Estados da federação ##########
data2 = pd.read_sql("""

            select Estado, label, quant from (
                    (select "SG_UF_ESC" as Estado,'Baixo' as label, count(*) as quant from enem2018 where "mediaTodos" < 600 and "SG_UF_ESC" is not null group by "SG_UF_ESC")  union
                    (select "SG_UF_ESC" as Estado, 'Alto' as label, count(*) as quant from enem2018 where "mediaTodos" >= 600 and "SG_UF_ESC" is not null group by "SG_UF_ESC") 
                )  t order by t.quant asc;

                     """, con=db)

#
# data = pd.read_sql("""
#                     select p.Estado, p.Media from (
#                         select "SG_UF_ESC" as Estado, avg("mediaTodos") as Media from enem2018 where "SG_UF_ESC" is not null group by "SG_UF_ESC"
#                         ) p  order by p.Media asc;
#
#                      """, con=db)
print(data2)