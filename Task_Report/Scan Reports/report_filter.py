import json
from pprint import pprint

def dependency_check_report():
    """
    {
        "isVirtual": false,
        
        "fileName": "express-fileupload:0.4.0",
        
        "filePath": "/var/lib/jenkins/workspace/node-app-pipeline/node_modules/express-fileupload/package.json",
        
        "md5": "643c794a5e505dcb6f9f5f15a5f653e0",
        
        "sha1": "5c7a25560f3b2b7e81d6b1877728987e661b8cea",
        
        "sha256": "b7d5f14898ab99fee90d49b158385e56f2dd309b6e7ba7ab998dbc2f56f7bf03",
        
        "description": "Simple express file upload middleware that wraps around Busboy",
        
        "license": "MIT",
        
        "projectReferences": [
            "dvna:0.0.1"
        ],

        "evidenceCollected": {

        "vendorEvidence": [
            {
                "type": "vendor",
                "confidence": "HIGH",
                "source": "package.json",
                "name": "name",
                "value": "express-fileupload"
            },
            {
                "type": "vendor",
                "confidence": "HIGHEST",
                "source": "package.json",
                "name": "author.name",
                "value": "Richard Girges"
            },
            {
                "type": "vendor",
                "confidence": "HIGHEST",
                "source": "package.json",
                "name": "author.email",
                "value": "richardgirges@gmail.com"
            }
        ],

        "productEvidence": [
            {
                "type": "product",
                "confidence": "HIGHEST",
                "source": "package.json",
                "name": "name",
                "value": "express-fileupload"
            },
            {
                "type": "product",
                "confidence": "HIGHEST",
                "source": "package.json",
                "name": "description",
                "value": "Simple express file upload middleware that wraps around Busboy"
            }
        ],

        "versionEvidence": [
            {
                "type": "version",
                "confidence": "HIGHEST",
                "source": "package.json",
                "name": "version",
                "value": "0.4.0"
            }
        ]
        },
        
        "packages": [
            {
                "id": "pkg:npm/express-fileupload@0.4.0",
                "confidence": "HIGHEST",
                "url": "https://ossindex.sonatype.org/component/pkg:npm/express-fileupload@0.4.0"
            }
        ],

        "vulnerabilities": [
            {
                "source": "NPM",
                "name": "1216",
                "severity": "low",
                "cwes": [],
                "description": "Versions of `express-fileupload` prior to 1.1.6-alpha.6 are vulnerable to Denial of Service. The package causes server responses to be delayed (up to 30s in internal testing) if the request contains a large `filename` of `.` characters.\n\n",
                "notes": "",
                "references": [
                {
                    "source": "Advisory 1216: Denial of Service",
                    "name": ""
                }
        ],
        
        "vulnerableSoftware": [
            {
                "software":
                {
                    "id": "cpe:2.3:a:*:express-fileupload:\\<1.1.6-alpha.6\\|\\|\\<\\=1.1.3-alpha.2\\|\\|\\<\\=1.1.2-alpha.1\\|\\|\\<\\=1.1.1-alpha.3\\|\\|\\<\\=1.0.0-alpha.1:*:*:*:*:*:*:*"
                }
            }
        ]
        },

        {
            "source": "OSSINDEX",
            "name": "CWE-400: Uncontrolled Resource Consumption ('Resource Exhaustion')",
            "severity": "HIGH",
            "cvssv3": {
            "baseScore": 7.5,
            "attackVector": "N",
            "attackComplexity": "L",
            "privilegesRequired": "N",
            "userInteraction": "N",
            "scope": "U",
            "confidentialityImpact": "N",
            "integrityImpact": "N",
            "availabilityImpact": "H",
            "baseSeverity": "HIGH"
            },

            "cwes": [
            "CWE-400"
            ],
            
            "description": "The software does not properly restrict the size or amount of resources that are requested or influenced by an actor, which can be used to consume more resources than intended.",
            
            "notes": "",
            
            "references": [
            {
                "source": "OSSINDEX",
                "url": "https://ossindex.sonatype.org/vuln/b5cc4326-6250-4a6d-ac4a-31954f0e8cf9",
                "name": "CWE-400: Uncontrolled Resource Consumption ('Resource Exhaustion')"
            }
            ],
            
            "vulnerableSoftware": [
            {
                "software": {
                "id": "cpe:2.3:a:*:express-fileupload:0.4.0:*:*:*:*:*:*:*",
                "vulnerabilityIdMatched": "true"
                }
            }
            ]
        }
        ]
    }
    """
    file_handler = open('dependency-check-report')
    json_data = json.loads(file_handler.read())

    file_handler.close()

    dependencies = json_data['dependencies']

    for dependency in dependencies:

        if 'vulnerabilities' in dependency:
            print('\n==============================================\n')
            print(dependency['fileName'] + ' : ' + dependency['vulnerabilities'][0]['severity'])


def snyk_report():
    """
    {'CVSSv3': 'CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H',
    'alternativeIds': [],
    'creationTime': '2019-10-22T12:22:54.665794Z',
    'credit': ['Roman Burunkov'],
    'cvssScore': 9.8,
    'description': '## Overview\n'
                    '\n'
                    '[express-fileupload](https://github.com/richardgirges/express-fileupload) '
                    'is a file upload middleware for express that wraps around '
                    'busboy.\n'
                    '\n'
                    '\n'
                    'Affected versions of this package are vulnerable to Denial of '
                    'Service (DoS).\n'
                    'The package does not limit file name length.\n'
                    '\n'
                    '## Details\n'
                    'Denial of Service (DoS) describes a family of attacks, all '
                    'aimed at making a system inaccessible to its intended and '
                    'legitimate users.\r\n'
                    '\r\n'
                    'Unlike other vulnerabilities, DoS attacks usually do not aim '
                    'at breaching security. Rather, they are focused on making '
                    'websites and services unavailable to genuine users resulting '
                    'in downtime.\r\n'
                    '\r\n'
                    'One popular Denial of Service vulnerability is DDoS (a '
                    'Distributed Denial of Service), an attack that attempts to '
                    'clog network pipes to the system by generating a large volume '
                    'of traffic from many machines.\r\n'
                    '\r\n'
                    'When it comes to open source libraries, DoS vulnerabilities '
                    'allow attackers to trigger such a crash or crippling of the '
                    'service by using a flaw either in the application code or '
                    'from the use of open source libraries.\r\n'
                    '\r\n'
                    'Two common types of DoS vulnerabilities:\r\n'
                    '\r\n'
                    '* High CPU/Memory Consumption- An attacker sending crafted '
                    'requests that could cause the system to take a '
                    'disproportionate amount of time to process. For example, '
                    '[commons-fileupload:commons-fileupload](SNYK-JAVA-COMMONSFILEUPLOAD-30082).\r\n'
                    '\r\n'
                    '* Crash - An attacker sending crafted requests that could '
                    'cause the system to crash. For Example,  [npm `ws` '
                    'package](npm:ws:20171108)\n'
                    '\n'
                    '## Remediation\n'
                    '\n'
                    'Upgrade `express-fileupload` to version 1.1.6-alpha.6 or '
                    'higher.\n'
                    '\n'
                    '\n'
                    '## References\n'
                    '\n'
                    '- [GitHub Fix '
                    'PR](https://github.com/richardgirges/express-fileupload/pull/171)\n',
    'disclosureTime': '2019-10-18T11:17:09Z',
    'exploit': 'Not Defined',
    'fixedIn': ['1.1.6-alpha.6'],
    'from': ['dvna@0.0.1', 'express-fileupload@0.4.0'],
    'functions': [],
    'functions_new': [],
    'id': 'SNYK-JS-EXPRESSFILEUPLOAD-473997',
    'identifiers': {'CVE': [], 'CWE': ['CWE-79'], 'NSP': [1216]},
    'isPatchable': False,
    'isUpgradable': True,
    'language': 'js',
    'modificationTime': '2019-11-20T09:48:38.528931Z',
    'moduleName': 'express-fileupload',
    'name': 'express-fileupload',
    'packageManager': 'npm',
    'packageName': 'express-fileupload',
    'patches': [],
    'publicationTime': '2019-10-22T15:08:40Z',
    'references': [{'title': 'GitHub Fix PR',
                    'url': 'https://github.com/richardgirges/express-fileupload/pull/171'}],
    'semver': {'vulnerable': ['<1.1.6-alpha.6']},
    'severity': 'high',
    'title': 'Denial of Service (DoS)',
    'upgradePath': [False, 'express-fileupload@1.1.6'],
    'version': '0.4.0'}
    """

    file_handler = open('snyk-report')
    json_data = json.loads(file_handler.read())
    file_handler.close()

    for vuln in json_data['vulnerabilities']:
        print('\n==============================================\n')
        print("Module/Package Name: " + vuln['moduleName'])
        print('Severity: ' + vuln['severity'])
        print('Title: ' + vuln['title'])


if __name__ == "__main__":
    # dependency_check_report()
    snyk_report()