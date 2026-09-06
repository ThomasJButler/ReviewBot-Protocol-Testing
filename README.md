# ReviewBot Protocol testing

Scratch repository for the hands-on test plan of [ReviewBot Protocol](https://github.com/ThomasJButler/ReviewBot-Protocol), a GitHub App that reviews pull requests with a language model running on the author's own machine. Every pull request here is a test scenario from that repository's docs/TEST_PLAN.md, run on 2026-09-06 and left open so the reviews can be read. Nothing in it is real code and no value in it is a real credential.

What to look at:

- [PR 1, the planted pull request](https://github.com/ThomasJButler/ReviewBot-Protocol-Testing/pull/1): an SQL injection, two made-up keys, an instruction planted in a comment for the reviewer to obey, a command injection, a `.env` file, a minified bundle and a rename. Four reviews, one per push: the first finds the planted lines, the second sees the SQL fix, the last is cross-examined by a second model family and shows where the two disagree.
- [PR 2, opened as a draft](https://github.com/ThomasJButler/ReviewBot-Protocol-Testing/pull/2): skipped while a draft, reviewed once marked ready, no findings on a clean file.
- [PR 3, thirty files](https://github.com/ThomasJButler/ReviewBot-Protocol-Testing/pull/3): twenty-five reviewed, five listed as over the file cap.

The reviews are comment reviews, never approvals, posted by `qwen3.5:9b` and `gemma4:12b` through Ollama on a laptop. Findings are model output and may be wrong; the point of the project is to read them and decide.
