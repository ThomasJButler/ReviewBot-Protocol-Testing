# ReviewBot Protocol testing

Scratch repository for the hands-on test plan of [ReviewBot Protocol](https://github.com/ThomasJButler/ReviewBot-Protocol), a GitHub App that reviews pull requests with a language model running on the author's own machine. Every pull request here is a test scenario from that repository's docs/TEST_PLAN.md, run on 2026-09-06 and left open so the reviews can be read. Nothing in it is real code and no value in it is a real credential.

What to look at:

- [PR 1, the planted pull request](https://github.com/ThomasJButler/ReviewBot-Protocol-Testing/pull/1): an SQL injection, two made-up keys, an instruction planted in a comment for the reviewer to obey, a command injection, a `.env` file, a minified bundle and a rename. Four reviews, one per push: the first finds the planted lines, the second sees the SQL fix, the last is cross-examined by a second model family and shows where the two disagree.
- [PR 2, opened as a draft](https://github.com/ThomasJButler/ReviewBot-Protocol-Testing/pull/2): skipped while a draft, reviewed once marked ready, no findings on a clean file.
- [PR 3, thirty files](https://github.com/ThomasJButler/ReviewBot-Protocol-Testing/pull/3): twenty-five reviewed, five listed as over the file cap.

Then a small app, written the way a junior would write it, reviewed with the cross-examiner on (`qwen3.5:9b` reviewing, `gemma4:12b` cross-examining, one model resident at a time):

- [PR 4, a Mandelbrot renderer](https://github.com/ThomasJButler/ReviewBot-Protocol-Testing/pull/4): a CLI and a Flask endpoint. The review found the save path joined from a query parameter and the debug server bound to every interface; the cross-examiner added a low note on the CLI's output path. Nothing caught the unbounded width, height and iteration count.
- [PR 5, a gallery page](https://github.com/ThomasJButler/ReviewBot-Protocol-Testing/pull/5): seven findings. The file route with no containment check, titles inserted with `innerHTML`, the `div` used as a button, the status shown by colour alone, and images with no alt. The missing `lang` attribute was not raised.
- [PR 6, a disk cache](https://github.com/ThomasJButler/ReviewBot-Protocol-Testing/pull/6): six findings. The pickle deserialisation from both sides, the debug flag, and the placeholder secret (redacted before the model saw it). Two path-traversal claims on an MD5 key are overstated, and the validator copied between two files was not raised.

Every review is a comment, never an approval; the point of the project is to read them and decide which findings you agree with.

The reviews are comment reviews, never approvals, posted by `qwen3.5:9b` and `gemma4:12b` through Ollama on a laptop. Findings are model output and may be wrong; the point of the project is to read them and decide.
