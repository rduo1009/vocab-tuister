#########################
 Setting the random seed
#########################

Randomness is used in various places in ``vocab-tuister``. Setting the seed for
the random module (using ``random.seed()``) is supported.

To do this, use the environment variable:

.. code:: console

   # Set the random seed
   export VOCAB_TUISTER_RANDOM_SEED=10

   # Unset the random seed
   unset VOCAB_TUISTER_RANDOM_SEED
