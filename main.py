# sockpuppet_agent/main.py
from agents.puppet_creator import generate_sock_puppet

if __name__ == "__main__":
    puppet = generate_sock_puppet(
        use_openai=True,
        use_local_llm=True,
        use_proxy=True
    )
    print("\nGenerated Sock Puppet:")
    print(puppet)
