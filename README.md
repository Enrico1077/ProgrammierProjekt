# ProgrammierProjekt

Backend fürs Programmier-Projekt

Development URL: https://development-ujgmkp4tpq-ez.a.run.app

Production URL: https://programmierprojekt-ujgmkp4tpq-ez.a.run.app

## Installation

To install the project's dependencies run the following command:

```
pip install -r requirements.txt
```

To add or remove dependencies from the project, edit the requirements.txt file and rerun the above command.

## Development

To lint all python files:

```
pylint app/*/*.py
```

Run unit tests locally:

```
pytest app/Tests/
```

Once the project's dependencies are installed, the project can be run in dev mode (it uses port 5000):

```
flask --app app run --debug
```

## Production

Run the app in production mode:

```
waitress-serve --port 5000 --host 0.0.0.0 --call app:create_app
```

## API

**Test API (HTTP GET):**

```
/hello
```

### k-Means API v2.0

To use the Euclidean distance:

```
/kmeans/euclidean
```

To use the Manhattan distance:

```
/kmeans/manhattan
```

The body must have a field called "file" which contains a .csv, .json, .xlsx or .xls file as value. __Please note the parameter csvDecimalSeparator to configure the display of decimal numbers correctly! Default setting is the European format!__
The API accepts the parameters shown in the table as query parameters. All parameters are optional! If a parameter is not specified, the default value given in the table is used.
The API returns the calculated data as a JSON object.

| parameter         | Description                                                                                                                     | Values                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| k                 | Number of centroids                                                                                                             | Integer, greater than zero<br>Default: Elbow algorithm          |
| normMethod        | Normalization method                                                                                                            | Default: None<br>1: Min-max normalization<br>2: z-normalization |
| r                 | Number of repetitions with different centroids                                                                                  | Integer, greater than zero<br>Default: 5                        |
| maxCentroidsAbort | Indication, after how many centroids the Elbow procedure is aborted                                                             | Integer, greater than zero<br>Default: 100                      |
| minPctElbow       | Minimum percentage deviation to detect an Elbow                                                                                 | Floating point number, 0 to 100<br>Default: 0                   |
| c                 | Number of cycles in the algorithm                                                                                               | Integer, greater than zero<br>Default: Dynamic                  |
| minPctAutoCycle   | With automatic number of cycles, specifies the minimum percentage improvement that must occur before another cycle takes place. | Floating point number, 0 to 100<br>Default: 0.5                 |
| maxAutoCycleAbort | Specifies after how many cycles to terminate at automatic cycle count, regardless of percentage improvement                     | Integer, greater than zero<br>Default: 25                       |
|sheetName|Specifies which worksheet of an Excel file is to be processed. |String with the name of the worksheet<br>Default: The first worksheet|
|csvDecimalSeparator|Specifies which decimal and thousands separator is used in CSV files.<br>EU: comma as decimal separator and dot as thousands separator.<br>US: Dot as decimal separator and comma as thousands separator.|string with *EU* or *US*<br>Default: EU|
|parallelCalculations|This parameter is intended for experts and should usually be left at its default value.<br>It can be specified how many calculations are executed simultaneously. This can improve the performance under certain circumstances. A value above eight usually does not bring any added value. |Integer, greater than zero<br>Default: 8|

Examples:

```
/kmeans/manhattan?k=10&normMethod=1&r=55&maxCentroidsAbort=15&minPctElbow=0.1&c=33&minPctAutoCycle=0.1&maxAutoCycleAbort=10&csvDecimalSeparator=EU
```
```
/kmeans/euclidean
```
```
