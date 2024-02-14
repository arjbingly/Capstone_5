from langchain_community.document_loaders import UnstructuredMarkdownLoader

def load_split_md(md_path, mode="single", strategy="hi-res", splitter=None):
    """
    Load and split data from a Markdown file.
    
    Parameters:
        md_path (str): Path to the Markdown file to be processed.
        mode (str, optional): Loading mode, defaults to "single".
        strategy (str, optional): Loading strategy, defaults to "hi-res".
        splitter (optional): Splitter instance to use for text splitting, defaults to None which uses RecursiveCharacterTextSplitter.
    
    Returns:
        md_doc: The loaded and split Markdown document, or None if an error occurs.
        
    """
    try:
        # Initiating Markdown loader
        md_loader = UnstructuredMarkdownLoader(md_path, 
                                               mode=mode,
                                               strategy=strategy)
        # Load and split the data
        md_doc = md_loader.load_and_split(splitter)
        return md_doc
    except Exception as e:
        # Handle or log the exception
        print(f"An error occurred: {e}")
        return None
#%% 
# Test case
load_split_md("C:\College\DSCI CAPSTONE\Capstone_5\code\Readme.md")