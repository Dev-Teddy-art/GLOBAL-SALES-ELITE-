import re

with open('src/components/ReferralTree.tsx', 'r') as f:
    content = f.read()

# Replace the closing div for the node card
content = content.replace(
'''              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}''',
'''              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}''')

with open('src/components/ReferralTree.tsx', 'w') as f:
    f.write(content)
