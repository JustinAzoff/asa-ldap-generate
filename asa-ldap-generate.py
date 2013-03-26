#!/usr/bin/env python

import ldap
import getpass

def get_groups(server, user, password, areas, filter="(CN=*VPN*)"):
    groups = []
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, 0)
    l = ldap.initialize(server, 0)
    l.simple_bind_s(user, password)

    for area in areas:
        groups.extend(l.search_s(area,ldap.SCOPE_SUBTREE, filter))

    return groups

def generate(map_name, server, user, password, areas, filter="(CN=*VPN*)"):
    groups = get_groups(server, user, password, areas, filter)
    vpn_groups = [g for g,info in groups if g and 'vpn -' in g.lower()]

    print 'ldap attribute-map', map_name

    profiles=[]
    for g in vpn_groups:
        gg = g.split(",")[0] # first comma part
        gg = gg.split(" - ",1)[1] # second part after - 
        gg = gg.replace(" ", '') # strip spaces
        profiles.append(gg)
        print ' map-value memberOf "%s" %s' % (g, gg)

    print

    for p in profiles:
        print "group-policy %s internal" % p
        print "group-policy %s attributes" % p
        print " address-pools value %s" % p.lower()
        print " banner value Welcome to the %s VPN Group" % p
        print

if __name__ == "__main__":
    import sys
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-s", "--server", dest="server", action="store", default="https://ldap",
                      help="LDAP Server URI 'https://..'")
    parser.add_option("-m", "--map", dest="map", action="store", default="ldap_map",
                      help="ldap attribute-map name")
    parser.add_option("-u", "--user", dest="user", action="store",
                      help="LDAP username")
    parser.add_option("-a", "--area", dest="areas", action="append",
                      help="one or more areas like DC=foo,DC=example,DC=com")
    parser.add_option("-f", "--filter", dest="filter", action="store", default="(CN=*VPN*)",
                      help="Search filter")
    (options, args) = parser.parse_args()


    if not options.user:
        parser.print_help()
        sys.exit(1)

    password = getpass.getpass("ldap password for %s:" % options.user)

    generate(options.map, options.server, options.user, password, options.areas, options.filter)
