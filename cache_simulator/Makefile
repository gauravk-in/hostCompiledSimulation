# Makefile for cache simulator

include Makefile.macros

check:
	$(MAKE) -C $(SRC_DIR) TARGET_DIR=$(TEST_DIR) all
	$(MAKE) -C $(TEST_DIR) all
	$(TEST_DIR)/cacheSimTest

check_clean:
	$(MAKE) -C $(TEST_DIR) clean