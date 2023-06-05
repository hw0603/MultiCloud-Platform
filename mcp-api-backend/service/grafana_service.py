import requests
import logging
import json
import datetime

logger = logging.getLogger("uvicorn")
dashboard_json_str = '''{
    "dashboard": {
    "annotations": {
        "list": [
            {
                "builtIn": 1,
                "datasource": {
                    "type": "grafana",
                    "uid": "-- Grafana --"
                },
                "enable": true,
                "hide": true,
                "iconColor": "rgba(0, 211, 255, 1)",
                "name": "Annotations & Alerts",
                "type": "dashboard"
            }
        ]
    },
    "description": "",
    "editable": true,
    "fiscalYearStartMonth": 0,
    "graphTooltip": 0,
    "links": [],
    "liveNow": false,
    "panels": [
        {
            "datasource": {
                "type": "mysql",
                "uid": "__DATASRC_UID__"
            },
            "description": "",
            "fieldConfig": {
                "defaults": {
                    "color": {
                        "mode": "palette-classic"
                    },
                    "custom": {
                        "axisCenteredZero": false,
                        "axisColorMode": "text",
                        "axisLabel": "",
                        "axisPlacement": "auto",
                        "barAlignment": 0,
                        "drawStyle": "line",
                        "fillOpacity": 70,
                        "gradientMode": "opacity",
                        "hideFrom": {
                            "legend": false,
                            "tooltip": false,
                            "viz": false
                        },
                        "lineInterpolation": "linear",
                        "lineStyle": {
                            "fill": "solid"
                        },
                        "lineWidth": 1,
                        "pointSize": 5,
                        "scaleDistribution": {
                            "type": "linear"
                        },
                        "showPoints": "auto",
                        "spanNulls": false,
                        "stacking": {
                            "group": "A",
                            "mode": "none"
                        },
                        "thresholdsStyle": {
                            "mode": "off"
                        }
                    },
                    "mappings": [],
                    "thresholds": {
                        "mode": "absolute",
                        "steps": [
                            {
                                "color": "green",
                                "value": null
                            },
                            {
                                "color": "red",
                                "value": 80
                            }
                        ]
                    },
                    "unit": "percent"
                },
                "overrides": []
            },
            "gridPos": {
                "h": 8,
                "w": 12,
                "x": 0,
                "y": 0
            },
            "id": 1,
            "options": {
                "legend": {
                    "calcs": [],
                    "displayMode": "list",
                    "placement": "bottom",
                    "showLegend": true
                },
                "timezone": [
                    "utc"
                ],
                "tooltip": {
                    "mode": "single",
                    "sort": "none"
                }
            },
            "targets": [
                {
                    "dataset": "mcp",
                    "datasource": {
                        "type": "mysql",
                        "uid": "__DATASRC_UID__"
                    },
                    "editorMode": "builder",
                    "format": "table",
                    "rawSql": "SELECT timestamp, value FROM mcp.aws_cloudwatch WHERE (metric = 'CPUUtilization' AND instance_id = '__INSTANCE_ID__') ORDER BY timestamp DESC LIMIT 600 ",
                    "refId": "A",
                    "sql": {
                        "columns": [
                            {
                                "parameters": [
                                    {
                                        "name": "timestamp",
                                        "type": "functionParameter"
                                    }
                                ],
                                "type": "function"
                            },
                            {
                                "parameters": [
                                    {
                                        "name": "value",
                                        "type": "functionParameter"
                                    }
                                ],
                                "type": "function"
                            }
                        ],
                        "groupBy": [
                            {
                                "property": {
                                    "type": "string"
                                },
                                "type": "groupBy"
                            }
                        ],
                        "limit": 600,
                        "orderBy": {
                            "property": {
                                "name": [
                                    "timestamp"
                                ],
                                "type": "string"
                            },
                            "type": "property"
                        },
                        "orderByDirection": "DESC",
                        "whereJsonTree": {
                            "children1": [
                                {
                                    "id": "bab88aab-0123-4456-b89a-b187fca58e7c",
                                    "properties": {
                                        "field": "metric",
                                        "operator": "equal",
                                        "value": [
                                            "CPUUtilization"
                                        ],
                                        "valueSrc": [
                                            "value"
                                        ],
                                        "valueType": [
                                            "text"
                                        ]
                                    },
                                    "type": "rule"
                                },
                                {
                                    "id": "b9abbb8a-cdef-4012-b456-7188014f7c8d",
                                    "properties": {
                                        "field": "instance_id",
                                        "operator": "equal",
                                        "value": [
                                            "__INSTANCE_ID__"
                                        ],
                                        "valueSrc": [
                                            "value"
                                        ],
                                        "valueType": [
                                            "text"
                                        ]
                                    },
                                    "type": "rule"
                                }
                            ],
                            "id": "8b9bb9ba-89ab-4cde-b012-3187fc9fbc56",
                            "type": "group"
                        },
                        "whereString": "(metric = 'CPUUtilization' AND instance_id = '__INSTANCE_ID__')"
                    },
                    "table": "aws_cloudwatch"
                }
            ],
            "title": "",
            "transparent": false,
            "type": "timeseries"
        },
        {
            "datasource": {
                "type": "mysql",
                "uid": "__DATASRC_UID__"
            },
            "description": "",
            "fieldConfig": {
                "defaults": {
                    "color": {
                        "mode": "palette-classic"
                    },
                    "custom": {
                        "axisCenteredZero": false,
                        "axisColorMode": "text",
                        "axisLabel": "",
                        "axisPlacement": "auto",
                        "barAlignment": 0,
                        "drawStyle": "line",
                        "fillOpacity": 70,
                        "gradientMode": "opacity",
                        "hideFrom": {
                            "legend": false,
                            "tooltip": false,
                            "viz": false
                        },
                        "lineInterpolation": "linear",
                        "lineStyle": {
                            "fill": "solid"
                        },
                        "lineWidth": 1,
                        "pointSize": 5,
                        "scaleDistribution": {
                            "type": "linear"
                        },
                        "showPoints": "auto",
                        "spanNulls": false,
                        "stacking": {
                            "group": "A",
                            "mode": "none"
                        },
                        "thresholdsStyle": {
                            "mode": "off"
                        }
                    },
                    "mappings": [],
                    "thresholds": {
                        "mode": "absolute",
                        "steps": [
                            {
                                "color": "green",
                                "value": null
                            },
                            {
                                "color": "red",
                                "value": 80
                            }
                        ]
                    },
                    "unit": "decbytes"
                },
                "overrides": []
            },
            "gridPos": {
                "h": 8,
                "w": 12,
                "x": 12,
                "y": 0
            },
            "id": 3,
            "options": {
                "legend": {
                    "calcs": [],
                    "displayMode": "list",
                    "placement": "bottom",
                    "showLegend": true
                },
                "timezone": [
                    "utc"
                ],
                "tooltip": {
                    "mode": "single",
                    "sort": "none"
                }
            },
            "targets": [
                {
                    "dataset": "mcp",
                    "datasource": {
                        "type": "mysql",
                        "uid": "__DATASRC_UID__"
                    },
                    "editorMode": "builder",
                    "format": "table",
                    "rawSql": "SELECT timestamp, value FROM mcp.aws_cloudwatch WHERE (metric = 'NetworkOut' AND instance_id = '__INSTANCE_ID__') ORDER BY timestamp LIMIT 200 ",
                    "refId": "A",
                    "sql": {
                        "columns": [
                            {
                                "parameters": [
                                    {
                                        "name": "timestamp",
                                        "type": "functionParameter"
                                    }
                                ],
                                "type": "function"
                            },
                            {
                                "parameters": [
                                    {
                                        "name": "value",
                                        "type": "functionParameter"
                                    }
                                ],
                                "type": "function"
                            }
                        ],
                        "groupBy": [
                            {
                                "property": {
                                    "type": "string"
                                },
                                "type": "groupBy"
                            }
                        ],
                        "limit": 200,
                        "orderBy": {
                            "property": {
                                "name": [
                                    "timestamp"
                                ],
                                "type": "string"
                            },
                            "type": "property"
                        },
                        "whereJsonTree": {
                            "children1": [
                                {
                                    "id": "bab88aab-0123-4456-b89a-b187fca58e7c",
                                    "properties": {
                                        "field": "metric",
                                        "operator": "equal",
                                        "value": [
                                            "NetworkOut"
                                        ],
                                        "valueSrc": [
                                            "value"
                                        ],
                                        "valueType": [
                                            "text"
                                        ]
                                    },
                                    "type": "rule"
                                },
                                {
                                    "id": "8ab8baaa-4567-489a-bcde-f188015499e3",
                                    "properties": {
                                        "field": "instance_id",
                                        "operator": "equal",
                                        "value": [
                                            "__INSTANCE_ID__"
                                        ],
                                        "valueSrc": [
                                            "value"
                                        ],
                                        "valueType": [
                                            "text"
                                        ]
                                    },
                                    "type": "rule"
                                }
                            ],
                            "id": "8b9bb9ba-89ab-4cde-b012-3187fc9fbc56",
                            "type": "group"
                        },
                        "whereString": "(metric = 'NetworkOut' AND instance_id = '__INSTANCE_ID__')"
                    },
                    "table": "aws_cloudwatch"
                }
            ],
            "title": "",
            "transparent": false,
            "type": "timeseries"
        },
        {
            "datasource": {
                "type": "mysql",
                "uid": "__DATASRC_UID__"
            },
            "description": "",
            "fieldConfig": {
                "defaults": {
                    "color": {
                        "mode": "palette-classic"
                    },
                    "custom": {
                        "axisCenteredZero": false,
                        "axisColorMode": "text",
                        "axisLabel": "",
                        "axisPlacement": "auto",
                        "barAlignment": 0,
                        "drawStyle": "line",
                        "fillOpacity": 70,
                        "gradientMode": "opacity",
                        "hideFrom": {
                            "legend": false,
                            "tooltip": false,
                            "viz": false
                        },
                        "lineInterpolation": "linear",
                        "lineStyle": {
                            "fill": "solid"
                        },
                        "lineWidth": 1,
                        "pointSize": 5,
                        "scaleDistribution": {
                            "type": "linear"
                        },
                        "showPoints": "auto",
                        "spanNulls": false,
                        "stacking": {
                            "group": "A",
                            "mode": "none"
                        },
                        "thresholdsStyle": {
                            "mode": "off"
                        }
                    },
                    "mappings": [],
                    "thresholds": {
                        "mode": "absolute",
                        "steps": [
                            {
                                "color": "green",
                                "value": null
                            },
                            {
                                "color": "red",
                                "value": 80
                            }
                        ]
                    },
                    "unit": "decbytes"
                },
                "overrides": []
            },
            "gridPos": {
                "h": 8,
                "w": 12,
                "x": 0,
                "y": 8
            },
            "id": 2,
            "options": {
                "legend": {
                    "calcs": [],
                    "displayMode": "list",
                    "placement": "bottom",
                    "showLegend": true
                },
                "timezone": [
                    "utc"
                ],
                "tooltip": {
                    "mode": "single",
                    "sort": "none"
                }
            },
            "targets": [
                {
                    "dataset": "mcp",
                    "datasource": {
                        "type": "mysql",
                        "uid": "__DATASRC_UID__"
                    },
                    "editorMode": "builder",
                    "format": "table",
                    "rawSql": "SELECT timestamp, value FROM mcp.aws_cloudwatch WHERE (metric = 'EBSWriteBytes' AND instance_id = '__INSTANCE_ID__') ORDER BY timestamp LIMIT 200 ",
                    "refId": "A",
                    "sql": {
                        "columns": [
                            {
                                "parameters": [
                                    {
                                        "name": "timestamp",
                                        "type": "functionParameter"
                                    }
                                ],
                                "type": "function"
                            },
                            {
                                "parameters": [
                                    {
                                        "name": "value",
                                        "type": "functionParameter"
                                    }
                                ],
                                "type": "function"
                            }
                        ],
                        "groupBy": [
                            {
                                "property": {
                                    "type": "string"
                                },
                                "type": "groupBy"
                            }
                        ],
                        "limit": 200,
                        "orderBy": {
                            "property": {
                                "name": [
                                    "timestamp"
                                ],
                                "type": "string"
                            },
                            "type": "property"
                        },
                        "whereJsonTree": {
                            "children1": [
                                {
                                    "id": "bab88aab-0123-4456-b89a-b187fca58e7c",
                                    "properties": {
                                        "field": "metric",
                                        "operator": "equal",
                                        "value": [
                                            "EBSWriteBytes"
                                        ],
                                        "valueSrc": [
                                            "value"
                                        ],
                                        "valueType": [
                                            "text"
                                        ]
                                    },
                                    "type": "rule"
                                },
                                {
                                    "id": "9899aa8a-cdef-4012-b456-71880155f31f",
                                    "properties": {
                                        "field": "instance_id",
                                        "operator": "equal",
                                        "value": [
                                            "__INSTANCE_ID__"
                                        ],
                                        "valueSrc": [
                                            "value"
                                        ],
                                        "valueType": [
                                            "text"
                                        ]
                                    },
                                    "type": "rule"
                                }
                            ],
                            "id": "8b9bb9ba-89ab-4cde-b012-3187fc9fbc56",
                            "type": "group"
                        },
                        "whereString": "(metric = 'EBSWriteBytes' AND instance_id = '__INSTANCE_ID__')"
                    },
                    "table": "aws_cloudwatch"
                }
            ],
            "title": "",
            "transparent": false,
            "type": "timeseries"
        }
    ],
    "refresh": false,
    "schemaVersion": 38,
    "style": "dark",
    "tags": [],
    "templating": {
        "list": [
            {
                "current": {},
                "definition": "",
                "hide": 0,
                "includeAll": false,
                "multi": false,
                "name": "query0",
                "options": [],
                "query": "",
                "refresh": 1,
                "regex": "",
                "skipUrlSync": false,
                "sort": 0,
                "type": "query"
            }
        ]
    },
    "time": {
        "from": "__PAST_TIME__",
        "to": "__CURRENT_TIME__"
    },
    "timezone": "utc",
    "title": "",
    "version": 1,
    "weekStart": ""
},
    "overwrite": true
}'''



async def create_dashboard(instance_id: str, provider_id: int, grafana_url: str, grafana_creds: str):
    # datasource 정보 가져오기
    req = requests.get(
        url=f"http://{grafana_creds}@{grafana_url}/api/datasources/name/MCP",
        headers={'Content-Type': 'application/json'}
    )
    data = req.json()
    logger.info(f"Grafana 서버 응답: {data}")
    datasource_uid = data.get('uid', None)

    # 대시보드 생성을 위한 정보 설정
    now = datetime.datetime.now()
    past = now - datetime.timedelta(hours=24)
    json_str = dashboard_json_str.replace(
        '__DATASRC_UID__', datasource_uid
    ).replace(
        '__INSTANCE_ID__', instance_id
    ).replace(
        '__CURRENT_TIME__', now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    ).replace(
        '__PAST_TIME__', past.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    )
    dashboard_json = json.loads(json_str)

    dashboard_json['dashboard']['title'] = instance_id
    dashboard_json['dashboard']['description'] = f"인스턴스 {instance_id} 의 대시보드"

    # 그라파나 대시보드 생성
    req = requests.post(
        url=f"http://{grafana_creds}@{grafana_url}/api/dashboards/db",
        json=dashboard_json,
        headers={'Content-Type': 'application/json'}
    )
    data = req.json()
    logger.info(f"Grafana 서버 응답: {data}")
    dashboard_uid = data.get('uid', None)
    dashboard_name = data.get('slug', None)

    return {
        "grafana_response": data,
        "dashboard_url": data.get('url', None),
        "dashboard_uid": dashboard_uid,
        "panel_urls": {
            "cpu": f"/d-solo/{dashboard_uid}/{dashboard_name}?orgId=1&refresh=25s&panelId=1",
            "network": f"/d-solo/{dashboard_uid}/{dashboard_name}?orgId=1&refresh=25s&panelId=2",
            "ebs": f"/d-solo/{dashboard_uid}/{dashboard_name}?orgId=1&refresh=25s&panelId=3",
        }
    }
