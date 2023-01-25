from emojipasta.generator import EmojipastaGenerator
import emojipasta.util.cli as cli
import subprocess

def main():
    args = cli.parse_arguments()
    generator = EmojipastaGenerator.of_default_mappings()
    pasta_str = generator.generate_emojipasta(args.string_to_parse)
    if args.commit:
        git_commit(pasta_str)
    else: 
        print(pasta_str)


def git_commit(commit_message):
    subprocess.run(['git', 'commit', '-m', commit_message])

if __name__ == "__main__":
    main()