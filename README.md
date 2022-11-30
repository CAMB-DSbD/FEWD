# FEWD
Fair Exchange Without Disputes

FEWD is a fair exchange protocol that prevents the occurrence of non-performance disputes. It always completes to produce either success or failure. The items are either successfully exchanged or the protocol is aborted. 

In FEWD, the two items under exchange need to remain concealed during the execution of the protocol until either both are revealed
to their receivers or deleted if the protocol is cancelled.

Therefore, FEWD is highly sensisitive to information exfiltration (leakage), therefore, it can benefit from memory compartmentalisation which can be implemented with CHERI capabilities. Therefore, in the CAMB project we will use it as a use case.
