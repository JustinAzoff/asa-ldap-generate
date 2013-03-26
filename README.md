ASA-LDAP-Generate
=================

Generate the ASA ldap map and group policies from LDAP.

Usage
-----

    asa-ldap-generate.py -s ldaps://ldap.example.com -u 'example\user' -a DC=groups,DC=example,DC=com

LDAP Setup
----------

This program assumes that VPN groups are created using the following format:

    CN=VPN - Group - Name

The ASA group policy will be named

    Group-Name

and the pool will be named

    group-name
