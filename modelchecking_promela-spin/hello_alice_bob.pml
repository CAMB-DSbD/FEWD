/* 
 * hello_alice_bob.pml
 * shows the basic concept of a Promela
 * program.
 * An process called alice sends a greeting message
 * to a process called bob, over a channel. Bob 
 * responds to alice's message over a return channel.
 * The code shows the use of :: guards in a
 * do-od loop.
 *
 * Programmer:
 * Carlos Molina-Jimenez (carlos.molina@cl.cam.ac.uk)
 * Departmet of Computer Science and Technology
 * University of Cambridge
 *
 * 23 sep 2025
 *
 * To run a random simulation of the model
 * https://spinroot.com/spin/Man/Spin.html
 *
 * % spin -s -r hello_alice_bob.pml
 * 7: proc  0 (alice:1) hello_alice_bob.pml:28 Sent How_r_u_Bob	-> queue 2 (ch_a2b)
 * ...
 */
 */

mtype= {How_r_u_Bob, Im_fine_Alice}; /* msg to send and receive */
chan ch_a2b= [0] of {mtype};   /* channel alice 2 bob     */
chan ch_b2a= [0] of {mtype};   /* channel bob to alice    */

/*
 * alice process sends (!) a msg to bob process
 * ans waits (?) for bob's reply.
 */
active proctype alice()
 {
  mtype a2b;  /* msg alice to bob */
  mtype b2a;  /* msg bob to alice */ 

  a2b= How_r_u_Bob;
  do
  :: ch_a2b ! a2b
  :: ch_b2a ? b2a -> break
  od;
  printf("\n alice recvd from bob msg: %e\n", b2a) 
 }

/*
 * bob process waits (?) to receive a msg from alice
 * process and sends (!) a respond.
 */
active proctype bob()
 {
  mtype a2b; /* msg alice to bob */
  mtype b2a; /* msg bob to alice */

  b2a= Im_fine_Alice;
  do
  :: ch_a2b ? a2b
  :: ch_b2a ! b2a -> break
  od;
  printf("\n bob recvd from alice msg: %e\n", a2b) 
 }


/*
 * spin init process:
 * It initiates single instances of ali and bob 
 */
init {
  run alice();
  run bob()
}

