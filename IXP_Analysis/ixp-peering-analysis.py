# Author: Arpit Gupta (glex.qsd@gmail.com)

ixp_member_fname = "ixp_members.txt"
ixp_2_member = {}
member_2_ixp = {}

def load_data():
    ''' Load the raw data to create ixp_2_member and member_2_ixp dicts'''
    with open(ixp_member_fname, 'r') as f:
        for line in f.readlines():
            tmp = line.split("\r\n")[0].split('\t')

            ixp, member = int(tmp[0]), int(tmp[1])
            if ixp not in ixp_2_member:
                ixp_2_member[ixp] = set()
            ixp_2_member[ixp] = ixp_2_member[ixp].union(set([member]))

            if member not in member_2_ixp:
                member_2_ixp[member] = set()
            member_2_ixp[member] = member_2_ixp[member].union(set([ixp]))


def get_ixp_with_max_partcipants(ixps_added):
    '''Get IXP with highest number of unique mem'''
    ixp_max = list(set(ixp_2_member.keys()).difference(set(ixps_added.keys())))[0]
    for ixp in ixp_2_member:
        if ixp not in ixps_added:
            if len(ixp_2_member[ixp]) > len(ixp_2_member[ixp_max]):
                ixp_max = ixp

    #print "ixp_max ", ixp_max, " participants: ", len(ixp_2_member[ixp_max])
    return ixp_max


def process_ixp_2_member(ixps_added, ixp_max):
    '''Remove participants already covered'''
    for ixp in ixp_2_member:
        if ixp not in ixps_added:
            # We need to update the unique member set for each of these IXPs
            ixp_2_member[ixp] = ixp_2_member[ixp].difference(ixp_2_member[ixp_max])


def incrementally_add_ixps():
    ixpCount_2_peers = {}
    total_participants = set()
    ixps_added = {}
    max_count = len(ixp_2_member.keys())

    for count in range(1,max_count+1):

        '''Start from the one with highest # of participants'''
        ixp_max = get_ixp_with_max_partcipants(ixps_added)
        initial = len(total_participants)
        total_participants = total_participants.union(ixp_2_member[ixp_max])
        delta = len(total_participants) - initial
        ixpCount_2_peers[count] = len(total_participants)
        ixps_added[ixp_max] = 0
        process_ixp_2_member(ixps_added, ixp_max)
        print "Count: ", count
        print "Added IXP ", ixp_max, " as it added ", delta, "unique networks"

    return ixpCount_2_peers


if __name__ == '__main__':
    load_data()
    ixpCount_2_peers = incrementally_add_ixps()
    print ixpCount_2_peers
