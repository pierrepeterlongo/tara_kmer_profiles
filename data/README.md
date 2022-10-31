## Command lines:
```
k=20
while IFS=' ' read -r line1 line2; do clean_line=`echo $line2 | tr -d ":" | tr -d  ";" `; ~/ntcard-1.2.2/ntcard -t 2 -k $k -p $1_${line1}_count_k$k ${clean_line}; done < $1.fof
```

### Note about datasets
Prepared by E. Pelletier on the TGGC.
Number of samples per fraction size: 

* 193 integrated (0.8-2000 and 3-2000)
* 208 meso (180-2000)
* 195 micro (20-280)
* 213 nano (3-20 and 5-20)
* 425 pico (0.2-0.45, 0.2-1.6, 0.22-3, 0.45-0.8, 0.8-3 an 0.8-5)
* 159 vir (0-0.2, 0.1-0.2)


### Note about k20
All sets ran with $k=20$ finished expected for the pico fraction where 345 sets over 425 had time to finish (24 hours computation max for all sets)

### Note about k25
For k25 I used only 2 hours per computation. Hence the number of computed sets is smaller:

* integrated 37 / 193  
* meso 38 / 208
* micro 34 / 195
* nano 35 / 213
* pico 36 / 425
* vir 51 / 159


 


