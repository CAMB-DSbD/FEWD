
/*
 22 sep 2025: carlos molina
 pbb_ali_bob.pml this version 
 includes the operation retrive that alice and
 bob can execute to retrieve the log from the
 PBB, called fsm_of_alice.
 
 Latest version of this code is in the folder
 romelaToGenerateSeqs22sep2025

 However, THE MODEL HAS A BUG (carlos.molina@cl.cam.ac.uk
 22 sep 2025): there is a set of trail
 files where model does not progress the pbb, alice
 or bob to success of cancel states.
 In these erroneous trail files, the model shows the
 log of the PBB but does not compute the synchronisation
 result.
 To find the error, it might be a good idea to execute
 the model in interactive mode to progress it from
 its initial state to the state the corresponds to the
 content of the PBB log.
 

 version 22 sep 2025
 Programmer: The Promela code was written by 
             MAILSON TELES BORGES <mailson.borges@sou.unijui.edu.br>

             carlos.molina@cl.cam.ac.uk used it to 
             generate all possible sequences
             that take Alice to success and cancel states.
 - success state: in the code it is called succ
 - cancel  state: in the code it is called canc
 
 I tested this code in
 Mac Book Pro with macOS Sequoia 15.6.1, 16GB
 Spin Version 6.5.2 -- 6 December 2019
 spin completes in less than 20 sec.

 
 Observation about the code:
 1) I tested it but not thoroughly. 
 2) The code is far from being clean or optimun: my aim 
    was to prove that Alice and Bob both reach
    either success or cancel and to generate the
    execution of messages *trail files that lead to
    these end states.
 3) The process "proctype fsm_of_alice()" is basically a PBB
 that 
 a) receives tokens posted by processes alice and Bob
 b) places the tokens in a log
 c) Computes (examines) the log to determine when process 
    alice reaches succ or canc.
 

A) To test for syntax errors
 =========================
 % spin -s pbb_ali_bob.pml
...


 B) To generate the sequeces that take Alice and Bob to
 their respective success states:
 ==========================================
 1- Generate an LTL that claims that alice and bob
    never reach their respective success states:
    ali_succ and bob_succ

% spin -f "<>(ali_succ && bob_succ)" 

never  {    <>(ali_succ && bob_succ) 
T0_init:
        do
        :: atomic { ((ali_succ && bob_succ)) -> assert(!((ali_succ && bob_succ))) }
        :: (1) -> goto T0_init
        od;
accept_all:
        skip
}


 2- Copy and paste the results to the end of the
    pbb_ali_bob.pml


 3- Compile to generate the spin model
 % spin -a pbb_ali_bob.pml

 4- Compile to generate the executable C code
 % gcc -o pan pan.c

 5- Generate the first 500 trail files that take alice 
    and bob to ali_succ and bob_succ  states.
    Spin generate less than 500 files if there are less
    path that take alice and bob to there success states. 

 % pan -a -e -c500 pbb_ali_bob.pml
   It generates 56 trail files


 6- Use
 % ls -l -S *.trail


 7- To examine  trail number 7 

spin -t7 -s -r pbb_ali_bob.pml


 C) To generate the sequeces that take Alice
    and bob to their respective cancel states 
 ==========================================
 1- Generate an LTL that claims that alice can never
    reach succ state
    ali_canc and bob_canc


% spin -f "[]!(ali_succ && bob_succ)" 
 never  {     []!(ali_succ && bob_succ) 

accept_init:
T0_init:
        do
        :: (! ((ali_succ && bob_succ))) -> goto T0_init
        od;
}




 2- Copy and past the results to the end of this
    file.


 3- Delete the LTL used for generating the sequeces that
    take alice to the canc state. Spin can work with
    only one LTL at a time.

 4- Process like in B) to examine to generate
    trail files and examine them,

 
spin -t7 -s -r pbb_ali_bob.pml
spin: trail ends after 395 steps
#processes: 4
		pbb_succ = 0
		pbb_canc = 1
		ali_succ = 0
		ali_canc = 1
		bob_succ = 0
		bob_canc = 1
		pbbLog[0] = sync_a
		pbbLog[1] = cancel_a
		pbbLog[2] = sync_b
		pbbLog[3] = 0
		pbbLog[4] = 0
		pbbLog[5] = 0
		aliLog[0] = sync_a
		aliLog[1] = cancel_a
		aliLog[2] = sync_b
		aliLog[3] = 0
		aliLog[4] = 0
		aliLog[5] = 0
		bobLog[0] = sync_a
		bobLog[1] = cancel_a
		bobLog[2] = sync_b
		bobLog[3] = 0
		bobLog[4] = 0
		bobLog[5] = 0
		pbbLogIndex = 3



5- Example of erroneus results produced by the bug

 
		pbbLog[5] = 0
		aliLog[0] = 0
		aliLog[1] = 0
		aliLog[2] = 0
		aliLog[3] = 0
		aliLog[4] = 0		aliLog[5] = 0
		bobLog[0] = 0
		bobLog[1] = 0
		bobLog[2] = 0
		bobLog[3] = 0
		bobLog[4] = 0
		bobLog[5] = 0
		pbbLogIndex = 4


*/



/* Mailson's wrote the following commented 9 lines
# compile the alice.pml file into C code
spin -a alice.pml
# generate the .exe file
gcc -o pan ./pan.c
# execute the model
./pan.exe -a -e -c500
 end Mailson's lines */


#define MAX_NUM_TOKENS 3

/* 
 * variables used by LTL formula for producing message sequences       
 */
bool pbb_succ = 0; /* pbb_succ and pbb_canc result computed by PBB */
bool pbb_canc = 0;  
bool ali_succ = 0; /* ali_succ and ali_canc: result computed by ali */ 
bool ali_canc = 0; 
bool bob_succ = 0; /* bob_succ and bob_canc: result computed by bob */
bool bob_canc = 0; 

mtype = {sync_a, cancel_a, sync_b, cancel_b};
mtype = {success, canceled, in_progress};
mtype = {retr_sync, retrieve_log, exchsucc, exchcanc};

chan channel = [0] of {mtype};

chan a2p_retr = [0] of {mtype}; /* alice to pbb chan for retrieve operation */
chan p2a_retr = [0] of {mtype}; /* pbb to alice chan for retrieve operation */
chan b2p_retr = [0] of {mtype}; /* bob to pbb chan for retrieve operation   */
chan p2b_retr = [0] of {mtype}; /* pbb to bob chan for retrieve operation   */

mtype pbbLog[(MAX_NUM_TOKENS * 2)];
mtype aliLog[(MAX_NUM_TOKENS * 2)];
mtype bobLog[(MAX_NUM_TOKENS * 2)];
byte  pbbLogIndex = 0;

/*
Iterate through the pbb and verify its current state:
canceled: either Alice or Bob has sent a cancellation token
success: Alice and Bob have agreed on the exchange
in_progress: the exchange is ongoing, and one or neither has sent the acceptance token
*/
inline get_pbb_current_state(result) {
    byte i = 0;

    bool is_cancel_b = false;
    bool is_cancel_a = false;
    bool is_sync_a = false;
    bool is_sync_b = false;
    atomic{
    do
    :: (i < (MAX_NUM_TOKENS * 2)) ->
        if
        :: (pbbLog[i] == cancel_a)  -> is_cancel_a = true
        :: (pbbLog[i] == cancel_b)  -> is_cancel_b = true
        :: (pbbLog[i] == sync_a)    -> is_sync_a = true
        :: (pbbLog[i] == sync_b)    -> is_sync_b = true
        fi;

        if
        :: (is_cancel_a)            -> result = canceled; break
        :: (is_cancel_b)            -> result = canceled; break
        :: (is_sync_a && is_sync_b) -> result = success; break
        :: else                     -> in_progress
        fi;

        i++

    :: else -> break
    od;}
}




/* 
Simulate Alice's FSM
*/
proctype fsm_of_alice()
{
    mtype token;
    mtype msg;
    mtype leftovermsg;
    mtype m2a;
    mtype m2b;
    mtype syncres;
    mtype current_state;
    byte k=0;
    byte j=0;
    bool ali_retrieved=0;
    bool bob_retrieved=0;

    S_init: channel?token ->
    printf("\n S_init: %e \n", token);

    pbbLog[pbbLogIndex]=token;
    pbbLogIndex++;

    atomic{
    if
    :: token == sync_a   -> goto S_ali_wish2exc
    :: token == cancel_a -> syncres= exchcanc;
                            goto S_retrieve
    :: token == sync_b   -> goto S_init
    :: token == cancel_b -> syncres= exchcanc;
                            goto S_retrieve 
    fi};

    S_ali_wish2exc: channel?token ->
    printf("\n S_ali_wish2exc: %e \n", token);

    pbbLog[pbbLogIndex]=token;
    pbbLogIndex++;
     
    atomic{
    if
    :: token == sync_a   -> goto S_ali_wish2exc
    :: token == cancel_a -> goto S_ali_wish2canc
    :: token == sync_b || token == cancel_b ->
        get_pbb_current_state(current_state);

        if
        :: (current_state == success) -> 
                             syncres= exchsucc;
                             goto S_retrieve
        :: (current_state == canceled) -> 
                             syncres= exchcanc;
                             goto S_retrieve
        :: else -> skip
        fi
    fi;}

    S_ali_wish2canc: channel?token ->
    printf("\n S_ali_wish2canc: %e \n", token);

    pbbLog[pbbLogIndex]=token;
    pbbLogIndex++;

    atomic{
    if
    :: token == sync_a   -> goto S_ali_wish2canc
    :: token == cancel_a -> goto S_ali_wish2canc
	:: token == sync_b || token == cancel_b ->
        get_pbb_current_state(current_state);

        if
        :: (current_state == success) -> syncres=exchsucc;
                                         goto S_retrieve
        :: (current_state == canceled)-> syncres=exchcanc;
                                         goto S_retrieve
        :: else -> printf("\n\n This is an error: wrong current_state\n\n")
        fi 

    fi};
    do
    /* :: false ->skip */
	:: printf("\n\n This is an error of current_state, fmd_of_alice should not reach this point\n\n")
    od;

/* empty (q) -> break https://spinroot.com/spin/Man/empty.html */

    S_retrieve:
    do
    :: channel ? leftovermsg -> 
       printf("\n\n leftovermsg=%e\n\n",leftovermsg)
    :: timeout -> 
       printf("\n\n non leftovermsg in channel\n\n");
       break
    od;

    ali_retrieved=0;
    bob_retrieved=0;
    do
    :: a2p_retr ? msg -> 
         if
         :: (msg==retr_sync) -> m2a=syncres; p2a_retr ! m2a
         :: else -> printf("\n\n a2p_retr recv: %e  wrong retr_sync msg\n",msg)
         fi;
       a2p_retr ? msg -> 
         if
         :: (msg==retrieve_log) -> /* m2a=pbblog; p2a_retr ! m2a*/
            k=0;
            do
            :: (k < (MAX_NUM_TOKENS * 2)) -> p2a_retr ! pbbLog[k]; 
                k++
            :: (k >= (MAX_NUM_TOKENS * 2)) ->  break 
            od
         :: else -> printf("\n\n a2p_retr recv: %e wrong retrieve_log msg\n",msg);
         fi;
         ali_retrieved=1

    :: b2p_retr ? msg ->  
         if
         :: (msg==retr_sync) -> m2b=syncres; p2b_retr ! m2b 
         :: else -> printf("\n\n b2p_retr recv: %e  wrong retr_sync msg\n",msg)
         fi;
         b2p_retr ? msg -> 
         if
         :: (msg==retrieve_log) -> /* m2b=pbblog; p2b_retr ! m2b */
            k=0;
            do
            :: (k < (MAX_NUM_TOKENS * 2)) -> p2b_retr ! pbbLog[k]; 
                k++
            :: (k >= (MAX_NUM_TOKENS * 2)) ->  break 
            od
            
         :: else -> printf("\n\n b2p_retr recv: %e  wrong retrieve_log msg\n",msg)
         fi;
         bob_retrieved=1
    :: (ali_retrieved==1 && bob_retrieved==1) -> 
       printf("\n\n yesssssssssssss  ali and bob have retrieved\n");
       break
    od;


    if
    :: atomic{(syncres == exchsucc) -> goto end_S_success}
    :: atomic{(syncres == exchcanc) -> goto end_S_cancel}
    fi;



    /* 18 sep 2025: carlos.molina@cl.cam.ac.uk
     * After reaching success or cancel, the PBB sends
     * the outmecome of the synchronisation to Alice and
     * Bob over chtoali and chtobob channels.
     */
    end_S_success:
	printf("\n end_S_success: %e \n", token);
    pbb_succ = 1; 
    do
    :: false -> skip
    od; 


    end_S_cancel:
    printf("\n end_S_cancel: %e \n", token);
    pbb_canc = 1;
    do
    :: false -> skip
    od; 
}



/* 
Simulate Alice's action of sending tokens
The last token is always a retrieve token
*/
proctype alice()
{
    mtype token;
    mtype syncres;
    mtype logres;
    mtype logelem; /* log element */
    mtype msg;
    mtype m;
    byte num_tokens = 0;
    byte k=0; 
    byte j=0;
    /* mtype aliLog[(MAX_NUM_TOKENS * 2)]; */

    do
    :: num_tokens < MAX_NUM_TOKENS - 1 ->
        if
        :: token = sync_a;
        :: token = cancel_a;
        fi;

        /* printf("\n\n Ali trying to send token\n"); */
        atomic{
        channel!token; num_tokens++;
        printf("\n\n ===============>Ali has sent num_tokens=%u \n\n", num_tokens);
        printf("\n\n          <<<token>>>%e<<</token>>>\n\n",token)
        }
    :: else ->  goto RetrieveAliS
    od;


/* 18 sep 20 25: carlos molina jimenez
 * Alice places a retrieve operation against the PBB
 * AT THE END of her execution to learn the result
 * of the synchronisation.
 * In a full implementation Alice should be able to
 * place retrieve operations at any time.
 */
RetrieveAliS: 
  printf("\n\n sssssssssssssss>Ali reached RetrieveAliS \n\n");
  m= retr_sync;
  a2p_retr ! m ->     printf("\n\n      <<<ali's msg>>>%e<<</ali's msg>>>\n\n",m);
  p2a_retr ? syncres; printf("\n\n      <<<ali's msg>>>%e<<</ali's msg>>>\n\n",syncres);
  printf("\n\n SYNCa res= %e \n\n", syncres);

  m= retrieve_log;
  a2p_retr ! m -> printf("\n\n          <<<ali's msg>>>%e<<</ali's msg>>>\n\n",m);
  /* p2a_retr ? logres; */
  /* printf("\n\n LOGa res= %e \n\n", logres); */
  k=0;
  do 
  :: (k < (MAX_NUM_TOKENS*2)) -> p2a_retr ? logelem; 
     aliLog[k]= logelem;
     printf("\n\n aliLog[%u]=%e\n", k, logelem); 
     k++
  :: else -> 
     j=0;
     do
     :: (j < (MAX_NUM_TOKENS*2)) ->
        printf("\n\n aliLog[%u]=%e\n", j, aliLog[j]); 
        j++
     :: else -> break
     od;
     break
  od; 

   
  printf("\n\n          <<<msg>>>Alice's retrieve<<</msg>>>\n\n");
  if
  :: (syncres==exchsucc) -> ali_succ=1; 
     goto end_succ_StateAlice

  :: (syncres==exchcanc) -> ali_canc=1; 
     goto end_canc_StateAlice
  :: else -> printf("\n\n Uknown error with Ali\n");
  fi;


end_succ_StateAlice: /* Alice final state: sucess */
 do
 :: false -> skip
 od;

end_canc_StateAlice: /* Alice final state: cancel */
 do
 :: false -> skip
 od
}


/* 
Simulate Bob's action of sending tokens
The last token is always a retrieve token
*/
proctype bob()
{
    mtype token;
    mtype syncres;
    mtype logelem; /* log element */
    mtype msg;
    mtype m;
    byte  num_tokens = 0;
    byte k=0;
    byte j=0;
    /* mtype bobLog[(MAX_NUM_TOKENS * 2)]; */


    do
    :: num_tokens < MAX_NUM_TOKENS - 1 ->
        if
        :: token = sync_b;
        :: token = cancel_b;
        fi;
        atomic{
        channel ! token; num_tokens++;
        printf("\n\n ===============>Bob has sent num_tokens=%u \n\n", num_tokens);
        printf("\n\n          <<<token>>>%e<<</token>>>\n\n",token) 
        }
    :: else -> goto RetrieveBobS 
    od;

/* 18 sep 20 25: carlos molina jimenez
 * Bob places a retrieve operation against the PBB
 * AT THE END of his execution to learn the result
 * of the synchonisation.
 * In a full implementation Bob should be able to
 * place retrieve operations at any time.
 */
RetrieveBobS: 
  printf("\n\n sssssssssssssss>Bob reached RetrieveBobS \n\n");
  m= retr_sync;
  b2p_retr ! m ->     printf("\n\n     <<<bob's msg>>>%e<<</bob's msg>>>\n\n",m);
  p2b_retr ? syncres; printf("\n\n     <<<bob's msg>>>%e<<</bob's msg>>>\n\n",syncres);
  printf("\n\n SYNCb res= %e \n\n", syncres);

  m= retrieve_log;

  b2p_retr ! m -> printf("\n\n     <<<bob's msg>>>%e<<</bob's msg>>>\n\n",m);
  /* p2b_retr ? logres; */
  /* printf("\n\n LOGb res= %e \n\n", logres); */
  k=0;
  do 
  :: (k < (MAX_NUM_TOKENS*2)) -> p2b_retr ? logelem; 
     bobLog[k]= logelem;
     printf("\n\n bobLog[%u]=%e\n", k, logelem); 
     k++
  :: else -> 
     j=0;
     do
     :: (j < (MAX_NUM_TOKENS*2)) ->
        printf("\n\n bobLog[%u]=%e\n", j, bobLog[j]); 
        j++
     :: else -> break
     od;
     break
  od; 


  if
  :: (syncres==exchsucc) -> bob_succ=1; 
     goto end_succ_StateBob

  :: (syncres==exchcanc) -> bob_canc=1; 
     goto end_canc_StateBob
  :: else -> printf("\n\n Uknown error with Bob\n");
  fi;


end_succ_StateBob: /* Bob final state: cancel */
 do
 :: false -> skip
 od;


end_canc_StateBob: /* Bob final state: cancel */
 do
 :: false -> skip
 od
}




init {
    run fsm_of_alice(); /* this is the PBB disguised as alice's fsm */
    run bob();
    run alice();
}




/* carlos@PromelaToGenerateSeqs14sep2025% spin -f "<>(ali_succ && bob_succ)" */
/* Carlos LTL 18 Sep 2025
 * produces msg sequences where both Alice and Bob
 * ends in their respective success states.
 * The states are represented by  variables
 * ali_succ = 1, ali_canc = 0, bob_succ = 1, bob_canc = 0
 * In the code, that these states are lables:
 * end_succ_StateAlice, end_canc_StateAlice
 * end_succ_StateBob, end_canc_StateBob
 */
/* never  {    *//* <>(ali_succ && bob_succ) */
/*T0_init:
	do
	:: atomic { ((ali_succ && bob_succ)) -> assert(!((ali_succ && bob_succ))) }
	:: (1) -> goto T0_init
	od;
accept_all:
	skip
}
*/


/* carlos@PromelaToGenerateSeqs14sep2025% spin -f "[]!(ali_succ && bob_succ)" */
/* Carlos LTL 18 Sep 2025
 * produces msg sequences where both Alice and Bob
 * ends in their respective cancel states.
 * The states are represented by  variables
 * ali_succ = 1, ali_canc = 0, bob_succ = 1, bob_canc = 0
 * In the code, that these states are lables:
 * end_succ_StateAlice, end_canc_StateAlice
 * end_succ_StateBob, end_canc_StateBob
 */
never  {    /* []!(ali_succ && bob_succ) */

accept_init:
T0_init:
	do
	:: (! ((ali_succ && bob_succ))) -> goto T0_init
	od;
}





/* 
 Mailson's LTL
Verifies that neither succ nor canc are true
*/
// never {    /* [](!succ && !canc) */
//     T0_init:
//         do
//         :: (!succ || !canc) -> goto violation
//         :: else -> skip
//         od;
//     violation:
//         assert(0)
// }



/* Verifies that either succ or canc is true */
/* never {   */ /* []( !(succ || canc) ) */
/*    T0_init:
        do
        :: (!(succ || canc)) -> goto T0_init
        :: else -> goto violation
        od;

    violation:
        assert(0)
}
*/



