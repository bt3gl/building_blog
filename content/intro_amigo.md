Title: Introducing Amigo, a tool to manage Google Cloud Platform Security
Date: 2017-12-17
Category: gcp, dev, h4x0r

![cyberpunk](./cyberpunk/27.jpg){:height="300px" width="400px"}


I wrote a tool called [Amigo](https://github.com/bt3gl/Amigo-Google-Cloud-Platform-Security) that uses the GCP API to fetch an organization's project data and with a set of customizable rules, it searches for security risks.

## How Amigo Works

Amigo retrieves the GCP project list and their attribute (defined in the `config.yaml` file).

#### Amigo perform two types of analysis:

**i)** For each attribute in a project, Amigo creates a up to date report. Amigo then checks the previous report for differences (or checking when the data was modified). If there is a diff, Amigo logs a report for this diff.

**ii)** Amigo saves the resources data in a database. Amigo then checks the custom rules specified in `rules.yaml` and reports everything that violates those rules.
Amigo performs two types of analytics, generating reports that can be fed in ELK/411:


## Setting up and Running Amigo

### Setting a Virtual Environment to install Amigo

```
$ make venv
# source venv/bin/activate
```

### Installing Amigo Package

```
$ make install
```

### Creating a Service Account for Amigo

This should be done once in the first time you set Amigo:

1. Create a project and a service account at [https://console.cloud.google.com/iam-admin/serviceaccounts](https://console.cloud.google.com/iam-admin/serviceaccounts).

2. Add the IAM roles **Security Reviewer** and **Viewer permissions** to the service account.

3. Download the **Service Account JSON credential file** to a safe directory (e.g. your home directory). If amigo runs in other machines (or other people in the same organization is running Amigo), this key can be shared (and step 1. and 2. do not need to be repeated).


### Setting gcloud

Install [gcloud SDK](https://cloud.google.com/sdk/downloads) and authenticate with:

```
$ gcloud auth application-default login
```

You can also check whether env variable `GOOGLE_APPLICATION_CREDENTIALS` is pointing to the **Service Account JSON credential file**.



### Setting the Config file

Copy `config.yaml_example` to `config.yaml` and customize it.

In the bottom of this file you are able to edit the attributes that you want to report on:
```
### Attributes to inspect
gcp_attributes:
    compute:
        - firewalls
        - networks
        - snapshots
```


### Setting the Rules file

Inspect `rules.yaml` either removing or adding rules that should be searched in the reports.


### Running Amigo

Run amigo with:

```
$ sudo amigo
```

This will retrieve the data from GCP and generate JSON reports. These reports will be save where is `reports_dir` in the config file.

It is advised to watch for STERR and STDOUT in the `log_file` file defined in `config.yaml` (default to `amigo_log.txt`):

```
$ tail -f amigo_log.txt
```

### Alerting on Amigo

Relevant reports (e.g. diff reports) are generated inside the directory defined as `results_dir`, in the file `results.log` (e.g. `/log/amigo.log`). This is a JSON file that can be fed to ELK.


----

## Creating Custom rules

### Firewalls Resource

Firewall reports have this format:

```
{
  "kind": "compute#firewall",
  "network": "https://www.googleapis.com/compute/v1/projects/<name>/global/networks/default",
  "direction": "INGRESS",
  "sourceRanges": [
    "0.0.0.0/0"
  ],
  "name": "default-allow-icmp",
  "priority": 65534,
  "allowed": [
    {
      "IPProtocol": "icmp"
    }
  ],
  "creationTimestamp": <Time stamp>,
  "id": <ID>,
  "selfLink": "https://www.googleapis.com/compute/v1/projects/<name>/global/firewalls/default-allow-icmp",
  "description": "Allow ICMP from anywhere"
}
```

### Networks Resource

Snapshot reports have this format:

```
{
  "kind": "compute#network",
  "description": "Default network for the project",
  "subnetworks": [
    "https://www.googleapis.com/compute/v1/projects/<name>/regions/<region>/subnetworks/default",
  ],
  "autoCreateSubnetworks": true,
  "routingConfig": {
    "routingMode": "REGIONAL"
  },
  "creationTimestamp": <Time stamp>,
  "id": <ID>,
  "selfLink": "https://www.googleapis.com/compute/v1/projects/<name>/global/networks/default",
  "name": "default"
}
```

### Snapshots Resource

Snapshot reports have this format:

```
{
  "status": "READY",
  "kind": "compute#snapshot",
  "storageBytes": <number>,
  "name": <name>,
  "sourceDisk": "https://www.googleapis.com/compute/v1/projects/<name>/zones/us-central1-c/disks/deployhost",
  "storageBytesStatus": "UP_TO_DATE",
  "labelFingerprint": <code>,
  "sourceDiskId": <ID>,
  "diskSizeGb": <size>,
  "licenses": [
    "https://www.googleapis.com/compute/v1/projects/centos-cloud/global/licenses/centos-7"
  ],
  "creationTimestamp": <time stamp>,
  "id": <ID>,
  "selfLink": "https://www.googleapis.com/compute/v1/projects/<name>/global/snapshots/snapshot-1-deployhost"
}
```

### Instance Template Resource

Instance Template reports have this format:


```
{
  "kind": "compute#instanceTemplate",
  "description": "",
  "properties": {
    "machineType": <type>,
    "tags": {
      "items": [
        <items>
      ]
    },
    "disks": [
      {
        "deviceName": "persistent-disk-0",
        "kind": "compute#attachedDisk",
        "initializeParams": {
          "sourceImage": "global/images/<name>",
          "diskType": "pd-standard"
        },
        "autoDelete": true,
        "index": 0,
        "boot": true,
        "mode": "READ_WRITE",
        "interface": "SCSI",
        "type": "PERSISTENT"
      }
    ],
    "scheduling": {
      "automaticRestart": true,
      "preemptible": false,
      "onHostMaintenance": "MIGRATE"
    },
    "serviceAccounts": [
      {
        "scopes": [
          "https://www.googleapis.com/auth/compute.readonly"
        ],
        "email": <service-account-email>
      }
    ],
    "networkInterfaces": [
      {
        "kind": "compute#networkInterface",
        "network": "https://www.googleapis.com/compute/v1/projects/<shared-vpn-name>/global/networks/etsy",
        "subnetwork": "https://www.googleapis.com/compute/v1/projects/<shared-vpn-name>/regions/us-central1/subnetworks/migration-test"
      }
    ],
    "metadata": {
      "items": [
        <metadata>
      "kind": "compute#metadata",
    }
  },
  "creationTimestamp": "2017-11-14T12:24:00.744-08:00",
  "id": <ID>
  "selfLink": "https://www.googleapis.com/compute/v1/projects/<project-name>/global/instanceTemplates/",
  "name": <name>
}
```


----

*** Thank you for reading, and let me know what you think!***
