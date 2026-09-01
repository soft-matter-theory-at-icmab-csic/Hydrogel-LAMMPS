set fp [ open "PEG-bonds.dat" w ]
puts $fp "## Number of linked bonds of each PEG with heparin"
for {set i 0} {$i < 223} {incr i} {
    set sel [atomselect top "residue $i and name 3 and within 1.6 of name 5"]
    set numero [$sel num]
    puts $fp "$i $numero"
}
close $fp
