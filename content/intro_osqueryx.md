Title: Introducing OsqueryX
Date: 2017-07-18
Category: osquery, security, elastalert, docker

![cyberpunk](./cyberpunk/28.jpg){:height="300px" width="400px"}


[osqueryX](https://github.com/bt3gl/osqueryx) is a set of tools to manage security data collection and alerts from [osquery](https://osquery.io/).


## Installing

Clone this repo and bootstrap your environment running:

```
$ make install
```

If you get a `Success!` message and you've finished the docker setup correctly, you should now be able start with:

```
$ osqueryx start
```


### Installation Notes

* If you can't get the script working (file a bug!) or install these manually:
    * Docker for Mac
    * Foreman

* Two temporary directories will be created under `osqueryx/tmp`, in order to help you start creating your first alerts:
        - tmp/elasticsearch - where Elasticsearch stores the index data.
        - tmp/log/osquery - where you can read your development logs for the OSQuery daemon.


* The following directories are mounted inside the ElastAlert container once it boots (ElastAlert reads rules and config from them):

        - `/opt/config`: ElastAlert (elastalert_config.yaml) and Supervisord (elastalert_supervisord.conf) configuration files.
        - `/opt/rules`: Contains ElastAlert rules.


----
## Starting


```
$ osqueryx start
```

This will start two docker containers (Elasticsearch/ElastAlert) in daemonized mode. You can check to see if they're running properly using 

```
$ docker ps
```

After the containers are booted, it will run `foreman start` to fire up OSQuery and Filebeat.

You should then be seeing the output of ElastAlert as it searches the Filebeat index in Elasticsearch.


----

## Creating a new osquery query

### Adding adhoc queries

OSQuery queries are added/modified in the `.conf` files in the `packs/` directory.

New JSON query file should be tested using `osqueryi` tool and linted with:

```
$ osqueryx lint_queries
```

Once you've modified the query pack you will have to restart the OSQuery process by hitting ```CTRL+C``` in the terminal where you're running foreman. Once you kill it, run:

```
$ osqueryx restart
```

### Adding malware queries

Malware queries (specified in the `packs/<OS>/malware.conf` file) are generate from YAML IoC files inside `iocs/<OS>/*`.

To add a new malware IoC/query/alert:

Add the IoC data inside the IoC type (e.g. `"bundle_id"`, `"process_name"`, `"launchdaemons"`) and generate the osquery queries with:
```
$ osqueryx create_queries
```

Once you've modified the query pack you will have to restart the OSQuery process by hitting ```CTRL+C``` in the terminal where you're running foreman. Once you kill it, run:

```
$ osqueryx restart
```


---
## Alerts

Alerts are generated using ElastAlert. ElastAlert reads all of the files in `rules/` and alerts when a document in the filebeat index matches. The files in `rules/` can be manually created or automatically generated.

You generate a list of alerts automatically with
```
$ osqueryx create_alerts
```

If you take a peek inside of `rules/` you will see a new YAML file for each query.

Once these files are added to `rules/` ElastAlert will pick them up on it's next config reload (every 60s).

---
## An Walk Through example

For instance, a new OSX indicator of compromise that is identified by a file `~/osquery_virus.txt` could be added to `iocs/osx/malicious_files.yaml` as:

```
the_osquery_virus_omg:
  - '/Users/%%/osquery_virus.txt'
```

Then, the OSQuery query (inside `malicious_files.conf`) and the alerts can be created by running:
```
$ osqueryx deploy
```

Restart osquery by hitting ```CTRL+C``` and then:

```
$ osqueryx restart
```

By default, OSQuery will run this query every hour. This can be customized by changing the value of the key **interval** in the top of the IoC YAML file (below **IoC Query Config**).

You can also add the desired type of ElastAlert alert there (e.g. "alert": "slack").

---

## Shipping your work

Whenever you are ready to push your work, you can bring osqueryx down with:

```
$ osqueryx stop
```

## More Details on How osqueryx Works

### ElastAlert variables in OSQuery

In order to generate our alerts automatically, we're storing some custom values inside of some queries. Since OSQuery stores it's config in JSON, we're able to add extra data to the Query objects and OSQuery will just ignore it. We're taking advantage of this and storing extra metadata about the kind of alert we'd like to generate.

Below is a table of supported attributes `osqueryx create_alerts` will add to the output of your alert.

| Query Key |     Type      |  Example |
|----------|:-------------:|------:|
| ElastAlert_rule_type |  string | new_term |
| ElastAlert_fields |    array   |   ["cats"] |


### Adding alerts

In most cases our alerts are generated directly from OSQuery queries, however, there will be some cases that we want to add an alert for some adhoc info that we want to know about.

Look in `examples/` to see what your ElastAlert should look like. Copy it into `rules/` and modify to your hearts content. Once you've got it working the way you want to then proceed to following the basic contribution steps for submitting the alert to this repo.


### Testing alerts

Before you commit your change in your PR, you should have tested the entire flow from start to finish for your alert. For example, if you want to add an OSQuery query which would alert you when a certain file existed on a users machine, create this query and alert in the osqueryx environment and then create the file. Once the file is created, OSQuery should write an event to the log file which should trigger ElastAlert.

By doing this, you should be able to see the alert and determine if it's what you intend. Also through this practice you can determine if this is a noisy alert and could use some tuning.


## Listing queries and alerts

Available queries can be listed with:
```
$ osqueryx list_queries
```

Available alerts can be listed with:
```
$ osqueryx list_alerts
```


#### OSQuery

**How does it run?**

OSQuery is booted up using Foreman which is executed when you run `osqueryx start`.

**Where can I read the logs?**

An automatic tail of these logs is started when you execute `osqueryx start`. The logs are prefixed with `OSQuery_log` in the foreman output. If you'd like to tail these logs separately, they live in `tmp/log/osquery`.

**How can I restart it?**

As with any Foreman controlled process, simply CTRL+C in the pane that you're running Foreman in and it will die. Simply run `foreman start` or `osqueryx start` to start up the processes again.

#### Filebeat

**How do I interact with it?**

Not much interaction should be required for Filebeat, however, if you desire to modify the config and restart the process, you would edit the config at `config/filebeat.yml` and then CTRL+C your Foreman and restart with `osqueryx start`.

**How does it run?**

Filebeat is booted up using Foreman which is executed when you run `osqueryx start`. If you want to run this process separately, look at the `osqueryx` command in the `Procfile`.

**Where can I read the logs?**

An automatic tail of these logs is started when you execute `osqueryx start`. The logs are prefixed with `filebeat_log` in the foreman output. If you'd like to tail these logs separately, they live at `tmp/filebeat/logs`.

**How can I restart it?**

As with any Foreman controlled process, simply CTRL+C in the pane that you're running Foreman in and it will die. Simply run `foreman start` or `osqueryx restart` to start up the processes again.


#### Elasticsearch

**How do I access it?**

Elasticsearch should be running at [http://localhost:9200](http://localhost:9200) after you run `osqueryx start`. From there you can interact with it using `curl` and the [Elasticsearch API](https://www.elastic.co/guide/en/elasticsearch/reference/2.4/docs.html).

**How does it run?**

Elasticsearch is started using Docker and Docker Compose. These commands are executed when you run `osqueryx start` which will bring the containers up in the background in a running state. Docker is used to encapsulate Elasticsearch in a Linux environment. This allows us to emulate an environment similar to production easily.

**Where can I read the logs?**

An automatic tail of these logs is started when you execute `osqueryx start`. The logs are prefixed with `elasticsearch_log` in the foreman output. If you'd like to tail these logs separately, you can do so by invoking the docker client on the terminal:

```
$ docker logs -f osqueryx_elasticsearch_1
```

**How can I restart it?**

Elasticsearch is run using Docker Compose. If you'd like to restart your running containers, you can run:

```
$ osqueryx restart
```

to issue a full restart of your containers. Keep in mind this will also restart ElastAlert.


**How do I know it's running?**

You can `curl localhost:9200` to see if Elasticsearch is listening on port 9200 properly. You should see something like this:

```
{
  "name" : "Commando",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "KflM016zREenHcjCrA4dfg",
  "version" : {
    "number" : "2.4.4",
    "build_hash" : "fcbb46dfd45562a9cf00c604b30849a6dec6b017",
    "build_timestamp" : "2017-01-03T11:33:16Z",
    "build_snapshot" : false,
    "lucene_version" : "5.5.2"
  },
  "tagline" : "You Know, for Search"
}
```

You can also look at your running containers by executing `docker ps | grep elasticsearch`:

```
$ docker ps  | grep elasticsearch
7f7e28471dbf        osqueryx_elasticsearch   "/elasticsearch_do..."   23 hours ago        Up 23 hours         0.0.0.0:9200->9200/tcp, 9300/tcp   osqueryx_elasticsearch_1
```

#### ElastAlert

**How do I interact with it?**

ElastAlert automatically detects rule changes on the filesystem and will reload rules accordingly. One magic thing we're doing in the osqueryx environment is mounting the ElastAlert `rules/` directory in this repo directly to `/opt/rules` in the container, which ElastAlert is configured to watch. Once you modify an alert, no restart of the service is required. Wait patiently and watch the logs for ElastAlert to reload your rule files.

**How does it run?**

ElastAlert is started using Docker and Docker Compose. The commands to bring up the Kibana container are executed when you run `osqueryx start`. You can check to see if it's running by executing:

```
$ docker ps | grep kibana
```

**Where can I read the logs?**

Foreman is set up to follow the tail of the logs which are generated by the container. If you'd like to tail this in a different window, you can run `docker logs -f osqueryx_elastalert_1` in a separate window to read the logs.


**How can I restart it?**

ElastAlert is run using Docker Compose. If you'd like to restart your running containers, you can run `osqueryx restart` to issue a full restart of your containers. Keep in mind this will also restart Elasticsearch.

#### Kibana

**How do I access it?**

Kibana should be running at [http://localhost:5601](http://localhost:5601) after you run `osqueryx start`.

**How does it run?**

Kibana is started using Docker and Docker Compose. The commands to bring up the Kibana container are executed when you run `osqueryx start`. You can check to see if it's running by executing `docker ps | grep kibana`.

**Where can I read the logs?**

An automatic tail of these logs is started when you execute `osqueryx start`. The logs are prefixed with `kibana_log` in the foreman output. If you'd like to tail these logs separately, you can do so by running `docker logs -f osqueryx_kibana_1`.

**How can I restart it?**

Kibana is run using Docker Compose. If you'd like to restart your running containers, you can run `osqueryx restart` to issue a full restart of your containers. Keep in mind this will also restart the other running containers that are defined in the `docker-compose.yml` file.


----


***Thank you for reading and let me know what you think!***