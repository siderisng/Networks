Networks 1st Assignment
========
Οδηγίες για τις εντολές που επιτρέπεται να πληκτρολογήσει ο Client παραθέτονται κατά την σύνδεση με το server. Συνοπτικά:
1) nFile<>*<Name of file>: Προσθέτει το αρχείο <Name of file> στη λίστα με τα διαθέσιμα αρχεία. Το όνομα πρέπει να ταιριάζει ακριβώς στο όνομα του αρχείου αλλιώς εμφανίζεται το μήνυμα "Something went wrong. Please try again. It's possible that client doesn't have file anymore.." 
2) tFile<><Name of file>: Ο client κάνει αίτηση για την παραλαβή ενός αρχείου που έχει ήδη ανεβεί. Σε περίπτωση επιτυχίας εμφανίζετα το μήνυμα "OK... FILE OBTAINED" στον παραλήπτη και στον αποστολέα "Just Sent a File". Διαφορετικά (και για τους λόγους αποτυχίας που αναφέραμε πιο πάνω) "Something went wrong. Please try again. It's possible that client doesn't have file anymore.." 
3) ShowList: Δείχνει τη λίστα με τα αρχεία προς διαμοιρασμό στον ενδιαφερόμενο client.
4)Q/q: Τερματίζει τον client.
5)Chat:<Message>:Χρησιμοποιείται για την αποστολή μηνύματος στους άλλους clients.
*<>: κενός χαρακτήρας

Κανόνες:
========

1)Το αρχείο στο nFile πρέπει να υπάρχει αλλιώς εμφανίζει μήνυμα λάθους.
2)Για την ομαλότερη εκτέλεση του προγράμματος προτείνουμε τη σύνδεση όλων των clients πριν αρχίσει η ανταλλαγή μηνυμάτων.
3)Απαραίτητο το κενό(<>) μετά τις εντολές nFile και tFile.

Παράδειγμα:
========
Παραθέτουμε την test.jpg για έλεγχο της λειτουργικότητας του προγράμματος τα βήματα είναι:
1)Άνοιγμα server και clients
2)Ανέβασμα αρχείου από κάποιο client με την εντολή nFile test.jpg
3)Αίτηση για λήψη της εικόνας από διαφορετικό client tFile test.jpg
4)Αναμονή για μήνυμα επιτυχίας από το πρόγραμμα
5)Άνοιγμα του αρχείου

