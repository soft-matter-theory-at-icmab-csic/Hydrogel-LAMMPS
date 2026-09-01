set fp [ open "heparin-bonds.dat" w ]
puts $fp "## Number of linked bonds of each heparin with PEG"
for {set i 223} {$i < 556} {incr i} {
    set sel [atomselect top "residue $i and name 5 and within 1.6 of name 3"]
    set numero [$sel num]
    puts $fp "$i $numero"
}
close $fp
