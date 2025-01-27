import random
import threading
import time


# Function that simulates the Part of Alice
def part_a(sync_value, shared_state, lock, done_event):
    print(f"Alice: Sending value C={sync_value} to Bob")

    # Alice sends the initial value of C to Bob
    with lock:
        shared_state['C'] = sync_value
        shared_state['message'] = "message from Alice"

    while sync_value > 0:
        # Alice is waiting for a message from Bob or timeout
        message_received = done_event.wait(timeout=2)  # Alice waits for the answer or timeout of 2 seconds

        with lock:
            if not message_received:
                print("Alice: Timeout - the synchronization failed.")
                return

            # Alice checks if a message was received from Bob
            if shared_state['message'] == "message from Bob":
                sync_value -= 1
                print(f"Alice: Received message from Bob, decrementing C to {sync_value}")

                if sync_value == 0:
                    print("Alice: Synchronization completed successfully!")
                    return

                # Alice sends a message back to Bob
                shared_state['message'] = "message from Alice"
                done_event.clear()  # Resets the event to wait for new message from Bob

    # Wait a timeout after the synchronization is complete
    done_event.wait(timeout=1)
    print("Alice: Synchronization successfully completed!")


# Function that simulates the Bob Part
def part_b(shared_state, lock, done_event):
    while True:
        time.sleep(1)  # Simula o tempo de espera entre mensagens

        with lock:
            if shared_state['message'] == "message from Alice":
                sync_value = shared_state['C']
                if sync_value > 0:
                    print("Bob: Recebida mensagem de Alice, enviando resposta...")
                    shared_state['message'] = "message from Bob"
                    done_event.set()  # Informa a Parte A que a mensagem foi recebida


def main():
    # Generate a random number for C
    random_value = random.randint(5, 10)

    # Shared status between Alice and Bob
    shared_state = {'C': random_value, 'message': None}

    # Lock to ensure synchronized access to shared state
    lock = threading.Lock()

    # Event to control the exchange of messages between Alice and Bob
    done_event = threading.Event()

    # Create the threads for Alice and Bob
    ga_thread = threading.Thread(target=part_a, args=(random_value, shared_state, lock, done_event))
    gb_thread = threading.Thread(target=part_b, args=(shared_state, lock, done_event))

    # Start the threads
    ga_thread.start()
    gb_thread.start()

    # Wait for the completion of the thread of Alice
    ga_thread.join()

    # End the thread of Bob
    print("Finalizing Bob’s process.")
    print("Alice' Attestable: Made release of Bob’s decrypted item to Alice!")
    print("Bob' Attestable: Made release of Alice’s decrypted item to Bob!")
    gb_thread.join(timeout=2)


if __name__ == "__main__":
    main()
