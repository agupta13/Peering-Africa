import profile
import pstats
profile.run('import bgp_prefixSearch; bgp_prefixSearch.main()', 'profile.tmp')
p = pstats.Stats('profile.tmp')
p.sort_stats('cumulative').print_stats(10)
