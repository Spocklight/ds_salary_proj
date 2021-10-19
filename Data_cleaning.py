#We import the CSV file directly from https://github.com/PlayingNumbers/ds_salary_proj/blob/master/glassdoor_jobs.csv
""" We weren't able to scrape the data by ourselves but we have 2 scripts that we could make work
We will go back to that later, right now we are gping to do the data cleaning
Enlace dónde pregunto cómo visualizar más cómodamente el dataframe, como en Spider -------> https://stackoverflow.com/questions/69604112/how-could-i-display-a-dataframe-from-sublime-text-into-a-console-to-better-explo
"""

import pandas as pd

#pd.set_option('display.max_columns', None) #Show every column when printing the data frame
#pd.set_option('expand_frame_repr', False)  #Shows dataframe in the same line
#pd.set_option('display.max_colwidth', None)

df = pd.read_csv('glassdoor_jobs.csv')
print("Tamaño del dataset: ", str(df.shape) +"\n"+ "Columnas del dataset: ", str(df.columns))
print(df)

print(df['Salary Estimate'].head(30)) #Tendremos que eliminar texto indeseado, símbolos y probablemente acabar convirtiéndolo en un int o float
print(df['Company Name'].head(5)) #Eliminaremos el número asociado a la compañia
print(df['Location'].head(5)) #Separaremos el estado asociado a la ubicacion
print(df['Founded'].head(5)) #También el año de creación por el número de años que lleva en activo
print(df['Job Description'].head(5)) #Parsing de esta columna (Pyhton, etc...)

#En la columna de salarios alunos están especificados por hora y otros por año. Además algunos elementos lo especifican con strings directamente

df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0) #Lower lo que hace es pasar todas las letras a minúscula. Así no tenemos que diferenciar entre unas y otras
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary' in x.lower() else 0)

#Eliinamos en Salary Estimate los valores -1 (que aon strings):

df = df[df['Salary Estimate'] != "-1"] #(!= No igual)
print(df.shape) #Pasamos de 956 a 742
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0]) #Utilizamos una función lambda para quedarnos solo con la primera parte de la columna 'Salary Estimate' Separador = '('
print(salary[0:5])
minus_Kd = salary.apply(lambda x: x.replace('K','').replace('$','')) #Limpiamos la columnda del símbolo del dolar y de la K
print(minus_Kd[0:5])

min_hour = minus_Kd.apply(lambda x: x.lower().replace('per hour', '').replace('employer provided salary:', '')) #Eliminamos esos strings
print(min_hour[0:30])

#Nos quedamos ahora con el máximo y con el mínimo en dos columnas diferentes:

df['min_salary'] = min_hour.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = min_hour.apply(lambda x: int(x.split('-')[1]))
df['avg_salary'] = (df.min_salary+df.max_salary)/2

#Company name text only:

df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis = 1) #Si tienen rating negativo no aparecen números. Si tienen rating positivo los último tres caracteres del company name vuelve a ser el rating
print(df['company_txt'][0:5])

#Estate Field

df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])
print(df['job_state'][0:5])
print(df.job_state.value_counts()) #Vemos cuántas ofertas hay por cada estado

#Creamos ahora una columna que indique si la empresa y la oferta se encuentran en el mismo estado

df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1)

#Número de años en activo: 

df['age'] = df.Founded.apply(lambda x: x if x<1 else 2020 - x) #Hay algunos elementos en los que no hay año d efundación (-1)
print(df.age[0:20])

print('-----------------')

#Parsing of job description:

#python 
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
print(df.python_yn.value_counts())

#r studio
df['r_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or 'r-studio' in x.lower() else 0)
print(df.r_yn.value_counts())

#spark
df['spark_yn'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
print(df.spark_yn.value_counts())

#aws
df['aws_yn'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
print(df.aws_yn.value_counts())

#excel
df['excel_yn'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
print(df.excel_yn.value_counts())

df_out = df.drop(['Unnamed: 0'], axis = 1)
df_out.to_csv('Salary_data_cleaned.csv', index = False)