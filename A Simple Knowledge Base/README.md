Your task in this assignment is to implement and test a definite clause theorem prover. Definite clauses are a subset of the regular propositional calculus that, while not as expressive as full propositional logic, they can be used to do very efficient reasoning.

Definition of Definite Clauses
A definite clause, or rule for short, is a propositional logic expression of this form:

head <-- b_1 & b_2 & b_3 ... & b_n
head, and b_1 to b_n are all ordinary propositional logic variables that are either true or false. We will usually call these atoms for short. The precise definition of legal atoms names is given in the function is_atom(s) given below.

n is an integer greater than, or equal to, 1. There must be exactly one atom, head, on the left of the <--.

& is logical “and”, i.e. the ordinary and operator from propositional logic.

<-- is the reverse of the usual propositional logic implication operator, i.e. X <-- Y means “Y implies X”.

The rule above cam be read “if b_1 and b_2 … and b_n are all true, then head is true``. Or, alternatively, “for head to be true, b_1 and b_2 … and b_n must all be true”. We will sometimes informally uses the word “prove” instead of “true” here, and say things like “to prove head is true, you must prove b_1 and b_2 … and b_n are all true”.

Note that there is no “not” or “or” in these rules, and so it is not possible to represent all propositional logic sentences as definite clauses.

Definition of a Knowledge Base File
For this assignment, a knowledge base file (KB file for short) consists of 1, or more, rules (as described above). For simplicity, we require that each rule be written on its own line. Blank spaces are permitted between rules, and extra whitespace is permitted around tokens.

So, for instance, here is a knowledge base file consisting of three rules:

snowing <-- cloudy & below_zero & white_stuff_falling

cloudy <-- no_sun & daytime

below_zero <-- very_cold
Logically speaking, the order in which we write the rules doesn’t matter, although you should try to group related ones together to increase readability.

For simplicity, you can assume that all rules in a KB file have a different head atom. In other words, you can assume that you will never have a situation like this:

cloudy <-- no_sun & daytime

cloudy <-- hard_to_see
Note

In this assignment, be careful how you use the words “true” and “false”. Informally, if an atom is in the KB then we can say it’s “true”, and if it’s not in the KB we can say it’s “false”. But just because an atom is in our KB doesn’t mean it is in fact true, and just because it is not in our KB doesn’t mean it is in fact false. For instance, a KB could contain an untrue fact like “it_raining” when it is not actually raining. Or a KB might not contain the atom “its_raining”, which does not mean it isn’t raining (it just means the agent doesn’t think it’s raining).

So, because of these concerns, it’s a good idea for this assignment to use the terms “in” and “out” instead of “true” or “false”

Definition of a Variable
The following function gives the precise definition of what strings can be used as atoms (i.e. variables) in definite clauses:

# returns True if, and only if, string s is a valid variable name
def is_atom(s):
    if not isinstance(s, str):
        return False
    if s == "":
        return False
    return is_letter(s[0]) and all(is_letter(c) or c.isdigit() for c in s[1:])

def is_letter(s):
    return len(s) == 1 and s.lower() in "_abcdefghijklmnopqrstuvwxyz"
Question 1: Interactive Interpreter
Implement an interpreter that lets a user interact with the KB. When run, your interpreter should display a prompt, e.g.:

kb>
It waits until the user enters a command (see below), and then tries to perform the command. If the user enters an invalid command, or the command cannot be run, then an error should be printed, e.g.:

kb> flurb
Error: unknown command "flurb"
Your interpreter should never crash: any error should just cause a helpful error message to be printed.

Your interpreter must implement (at least) these commands:

load someKB.txt: This loads into memory the KB stored in the file someKB.txt; of course, you can replace the name someKB.txt with whatever the name of the KB file is. For example:

kb> load sample1.txt
   snowing <-- cloudy & below_zero & white_stuff_falling
   cloudy <-- no_sun & daytime
   below_zero <-- very_cold

   3 new rule(s) added
If a KB file already happens to have been loaded, then calling load again will delete the old one and replace it with the new one.

If you try to load an incorrectly formatted KB file, then an error is printed. For example:

kb> load sample2.txt
Error: sample2.txt is not a valid knowledge base
tell atom_1 atom_2 ... atom_n: This adds the atoms atom_1 to atom_n to the current KB. For example:

kb> tell a b c d
  "a" added to KB
  "b" added to KB
  "c" added to KB
  "d" added to KB
If some atom_i is invalid (according to is_atom), then don’t add any variables and print an error message, e.g.:

kb> tell a b 4c d
Error: "4c" is not a valid atom
n is an integer greater than 1. It’s an error to type just “tell”, e.g.:

kb> tell
Error: tell needs at least one atom
If you tell an atom that is already in the KB (due to a previous tell command, or because it was inferred by the rules), then tell should say something like “atom X already known to be true”. For example:

kb> tell sunny
  "sunny" added to KB

kb> tell sunny
  atom "sunny" already known to be true
infer_all: Prints all the atoms that can currently be inferred by the rules in the KB. Note that no atoms can be inferred until at least one tell command is called.

When infer_all finishes, print all the inferred atoms, and clearly label them as inferred. Also, list and clearly label all the atoms that were known to be true before calling infer_all.

For example:

kb> load sample1.txt
  3 definite clauses read in:
   snowing <-- cloudy & below_zero & white_stuff_falling
   cloudy <-- no_sun & daytime
   below_zero <-- very_cold

kb> tell no_sun
  "no_sun" added to KB

kb> infer_all
  Newly inferred atoms:
     <none>
  Atoms already known to be true:
     no_sun

kb> tell daytime
  "daytime" added to KB

kb> infer_all
  Newly inferred atoms:
     cloudy
  Atoms already known to be true:
     no_sun, daytime

kb> infer_all
  Newly inferred atoms:
     <none>
  Atoms already known to be true:
     cloudy, no_sun, daytime

kb> tell very_cold white_stuff_falling
  "very_cold" added to KB
  "white_stuff_falling" added to KB

kb> infer_all
  Newly inferred atoms:
     below_zero snowing
  Atoms already known to be true:
     cloudy, daytime, no_sun, very_cold, white_stuff_falling
Note that you can add other commands if you like. For instance, a command like “clear_atoms” that removes all atoms might be useful for debugging.
