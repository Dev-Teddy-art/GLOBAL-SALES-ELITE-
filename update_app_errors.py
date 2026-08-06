import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

# Replace first catch
old_catch_1 = """    } catch (err: any) {
      setErrorMsg(err.message || 'Invalid email or password.');
    } finally {"""

new_catch_1 = """    } catch (err: any) {
      setErrorMsg(err.message || String(err));
      console.error("SANITY DB ERROR:", err);
    } finally {"""

content = content.replace(old_catch_1, new_catch_1)

old_catch_2 = """    } catch (err: any) {
      setErrorMsg(err.message || 'An error occurred during sign up. Please try again.');
    } finally {"""

new_catch_2 = """    } catch (err: any) {
      setErrorMsg(err.message || String(err));
      console.error("SANITY DB ERROR:", err);
    } finally {"""

content = content.replace(old_catch_2, new_catch_2)

with open('src/App.tsx', 'w') as f:
    f.write(content)
